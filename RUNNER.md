# Running the Evaluation Runner

`runner.py` compares LLM-generated levels against a non-LLM baseline for every
variant in `variants.py`. The baseline is built by `genetic.py`, a genetic
algorithm that evolves random content towards higher quality/controlability
(see [How the GA baseline works](#how-the-ga-baseline-works) below) instead of
just sampling random noise.

For each variant it:
1. loads the LLM-generated maps from `pcg_results.json`,
2. evolves a same-size GA baseline, one map per control target,
3. evaluates both with the benchmark (quality / diversity / controlability),
4. writes the combined metrics to `eval_results.json`,
5. renders both sets of maps to PNGs (`{key}_llm_{i}.png` / `{key}_pcg_{i}.png`).

## Prerequisites

From the repo root (`tools/pcg_benchmark/pcg_benchmark`), install the package
and its dependencies (`numpy`, `PIL`) once:

```
pip install -e .
```

You also need a `pcg_results.json` with the LLM output. Its keys must match
the `json_prefix` values declared in `variants.py` (e.g. `"binary-v0_0"`,
`"binary-v0_1"`, ...). By default the runner looks for it one directory up
(`../pcg_results.json`, i.e. `tools/pcg_benchmark/pcg_results.json`).

## Quick start

```
cd tools/pcg_benchmark/pcg_benchmark
python runner.py
```

This reads `../pcg_results.json` and writes `eval_results.json` plus the
rendered PNGs into the current directory.

## Fitting it into the `Iterations/` + report workflow

The report is **not** part of this repo. It lives in
`tools/pcg_benchmark/LLM_Game_Level_Generator_Benchmark_Results_Page`, a nested
checkout of its own git repo that GitHub Pages deploys from. `report.py` builds
the HTML comparison report from the numbered folders under that checkout's
`Iterations/`, then commits and pushes it to `main`, which triggers the Pages
redeployment -- so the published page always reflects the newest iteration.

Two reports are published side by side, cross-linked (each one's home page
links to the other via `--sibling-label`/`--sibling-href`), and reachable from
the bare Pages URL through a chooser landing page (see `publish.py`):

| Track | Iterations live in | `--track` value |
| --- | --- | --- |
| Reasoning model (default) | `Iterations/` | `reasoning` |
| Non-reasoning (gpt-4.1) | `Iterations/nonreasoning/` | `nonreasoning` |

To add a new iteration:

```
cd tools/pcg_benchmark/pcg_benchmark
python runner.py --iteration <N> --seed 1
python report.py
```

add `--track nonreasoning` to both commands to add it to the non-reasoning
report instead (and point `report.py --iterations` at
`../LLM_Game_Level_Generator_Benchmark_Results_Page/Iterations/nonreasoning`,
since `--track` is a `runner.py`-only flag -- `report.py`'s own `--iterations`
already says which report to build).

`--iteration <N>` writes straight into the results page repo
(`.../LLM_Game_Level_Generator_Benchmark_Results_Page/Iterations/<N>`, or
`Iterations/nonreasoning/<N>` with `--track nonreasoning`), so you don't have
to spell out `--output-dir`. `report.py` then picks it up, skips iterations
that already have a page (so it's safe to run after every run), and publishes.

The publish step (`publish.py`) also makes sure the Pages repo root has the
files Pages needs -- `.nojekyll`, and a chooser `index.html` linking to both
reports -- (re)writing them on every publish.

### Publish options

| Flag | Default | Meaning |
| --- | --- | --- |
| `--no-publish` | off | Build the pages but don't commit/push. Use when iterating locally. |
| `--remote NAME` | `origin` | Remote of the results page repo to push to. |
| `--branch NAME` | `main` | Branch Pages deploys from; the push always targets it (`HEAD:main`) whatever the local branch is called. |
| `--message TEXT` | generated | Commit message; defaults to `Add iteration <N>: <title from Iteration Control.txt>`. |

If the push fails (no network, needs a `git pull`, auth), `report.py` says so
and exits non-zero -- the pages are already built, so re-running after fixing
the cause (or committing the checkout by hand) is enough to publish them.

An iterations folder outside the Pages checkout (`--iterations` pointing
elsewhere) is built but never published.

## CLI options

**General**

| Flag | Default | Meaning |
| --- | --- | --- |
| `--results PATH` | `../pcg_results.json` | Path to the LLM output file. |
| `--output-dir DIR` | `.` | Where to write `eval_results.json` and the PNGs. |
| `--seed N` | random | Seeds both content sampling and the GA's own randomness, for reproducible runs. |
| `--workers N` | `os.cpu_count()` | Worker processes used to evolve GA baselines in parallel. |

**Genetic algorithm tuning** — all optional, defaults live in `genetic.py`:

| Flag | Default | Meaning |
| --- | --- | --- |
| `--population-size N` | 24 | Number of individuals evolved per map. |
| `--generations N` | 25 | Number of generations before the polish pass. |
| `--crossover-rate F` | 0.7 | Probability a child comes from crossing two parents (vs. cloning one). |
| `--mutation-rate F` | 0.08 | Per-gene probability of mutation after crossover/cloning. |
| `--elite-count N` | 2 | Top individuals carried over unchanged each generation. |
| `--tournament-size N` | 3 | Individuals sampled per tournament selection. |
| `--polish-iterations N` | 300 | Hill-climb steps applied to the best individual once evolution finishes. |

Example: a faster, lower-fidelity smoke test —

```
python runner.py --population-size 10 --generations 10 --polish-iterations 50
```

Example: a stronger (slower) run for a hard problem like `smbtile` —

```
python runner.py --population-size 48 --generations 60 --polish-iterations 500
```

## How the GA baseline works

For every LLM map, `runner.py` samples a control target and calls
`genetic.evolve_content(env, control)`, which:

1. Samples an initial population of random content (`env.content_space.sample()`).
2. Each generation, breeds children via tournament selection + uniform
   crossover/mutation (`contentSwap`, the framework's built-in recombination
   helper — see the top-level `README.md`'s "Creating a Generator" section),
   evaluating each child's `quality`/`controlability` and keeping the fittest.
3. Stops early once a perfect individual is found, otherwise runs for
   `--generations` rounds.
4. Runs a short hill-climb "polish" pass on the best individual
   (`--polish-iterations`) to finish converging on easy/smooth problems.

This works unmodified across every problem in the benchmark — plain tile
grids (`binary`, `zelda`, `sokoban`, `mdungeons`, `smbtile`, ...) as well as
dict-shaped content (`isaac`) — because it's written purely against the
`content_space` interface every problem already exposes.

### Expectations by problem difficulty

- **Small/smooth problems** (`binary`, `zelda`, `sokoban`, `mdungeons`,
  `loderunner`): the default settings reliably reach high average quality
  (roughly 0.9-1.0) and coherent, structured maps.
- **`smbtile` (Mario)**: a huge (`10^2400`) tile search space gated behind an
  all-or-nothing whole-level playability simulation. The GA makes real
  structural progress over random noise, but won't reliably reach full
  quality with the defaults — bump `--population-size`/`--generations` (and
  accept a much longer runtime) if you need stronger Mario baselines.

## Runtime

GA baseline generation -- the expensive part of a run -- is parallelized
across a `ProcessPoolExecutor` (real OS processes, not threads, so it isn't
limited by the GIL). Every `(variant, control)` GA task across *all*
variants is flattened into one pool up front rather than parallelizing each
variant separately, since per-variant map counts are small and uneven (some
variants only have 1-2 LLM maps) -- flattening keeps workers busy across the
whole run instead of idling on the low-count variants. Use `--workers` to
tune the pool size (defaults to `os.cpu_count()`); lower it if you're memory
constrained (each worker builds its own env, which is heavier for
`smbtile`/`mdungeons-large`).

A full run across every variant in `variants.py` takes roughly 5-10 minutes
single-threaded with the default settings (machine-dependent, and dominated
by the larger `smbtile`/`mdungeons-large` variants); wall-clock scales down
with `--workers`/available cores. Lower `--population-size`/`--generations`/
`--polish-iterations` for a quicker smoke test.

Note: with `--seed` set, results are reproducible run-to-run (each GA task
gets an independent RNG stream derived deterministically from the seed), but
they are *not* bit-identical to a single-process/pre-parallelization run
with the same seed -- the RNG consumption pattern is different by design so
that parallel tasks don't correlate with each other.
