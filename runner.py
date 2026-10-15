"""Evaluate LLM-generated levels against a non-LLM baseline.

For every variant in ``variants.VARIANTS`` this script:

  1. loads the LLM-generated maps from ``pcg_results.json``,
  2. builds a same-size baseline with the chosen ``--baseline`` generator --
     ``noise`` (a bare ``env.content_space.sample()``: unconstrained per-tile
     noise, no evolution or synthesis at all), ``ga``
     (``genetic.evolve_content``: evolves a population of random content
     towards higher quality/controlability), or ``wfc``
     (``wfc.generate_content``: Wave Function Collapse, synthesized from a
     small corpus of example maps -- see ``../ALGORITHM_RESEARCH.md``).
  3. evaluates both with the benchmark (quality / diversity / controlability)
     using a shared set of control targets so the comparison is fair,
  4. writes the combined metrics to ``eval_results.json``, and
  5. renders both the LLM and the baseline maps to PNG files.

The whole thing is driven by the single ``VARIANTS`` table, so adding or
removing a variant is a one-line change in ``variants.py``.

Baseline generation (the expensive part) runs across a process pool -- see
``_baseline_worker`` and ``run_baselines`` -- so it uses true multi-core
parallelism instead of being limited by the GIL under threads.

Iteration output belongs in the ``LLM_Game_Level_Generator_Benchmark_Results_Page``
checkout (the GitHub Pages repo), so prefer ``--iteration N`` over spelling out
``--output-dir``: it resolves to that repo's ``Iterations/N`` folder, where
``report.py`` will pick it up and publish it (see ``publish.py``).

Usage:
    python runner.py [--results PATH] [--output-dir DIR | --iteration N] [--seed N]
                      [--workers N] [--baseline {noise,ga,wfc}]
                      [--population-size N] [--generations N]
                      [--crossover-rate F] [--mutation-rate F]
                      [--elite-count N] [--tournament-size N]
                      [--wfc-corpus-size N] [--wfc-corpus-population N]
                      [--wfc-corpus-generations N]
                      [--wfc-corpus-polish-iterations N]
                      [--wfc-max-restarts N] [--wfc-polish-iterations N]
"""

import argparse
import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

import pcg_benchmark
import genetic
import publish
import wfc
from variants import VARIANTS, VARIANTS_BY_PREFIX


def convert_to_int_array(array: "list[list[str]]") -> "list[list[int]]":
    """Convert a 2D array of stringy numbers into ints."""
    return [[int(value) for value in row] for row in array]


def to_jsonable(obj):
    """Recursively turn numpy types into plain Python so ``json`` can dump them.

    Handles numpy scalars, numpy arrays, and arbitrarily nested
    dict / list / tuple structures (which is what ``details`` and ``infos``
    are made of, regardless of which game produced them).
    """
    if isinstance(obj, dict):
        return {key: to_jsonable(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(value) for value in obj]
    if isinstance(obj, np.ndarray):
        return to_jsonable(obj.tolist())
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def parse_results(results_path: str) -> "dict[str, list]":
    """Load and bucket the LLM-generated maps by variant.

    Keys in the results file look like ``"{json_prefix}_{index}"`` (e.g.
    ``"binary-v0_12"``); the index is separated by an underscore, so we split on
    the last ``_``. This keeps working for indices >= 10 (the old ``[:-2]``
    slice broke there).
    """
    contents = {variant.key: [] for variant in VARIANTS}

    with open(results_path, "r") as f:
        data = json.load(f)

    for result_key, raw_map in data["Output"].items():
        try:
            level = convert_to_int_array(raw_map)
        except (ValueError, TypeError):
            print(f"Error converting {result_key} to integer array")
            continue

        prefix = result_key.rsplit("_", 1)[0]
        variant = VARIANTS_BY_PREFIX.get(prefix)
        if variant is None:
            print(f"Unknown content key: {result_key}")
            continue

        contents[variant.key].append(level)

    return contents


def _baseline_worker(task):
    """Generate one baseline map. Runs in a worker process (see ``run_baselines``).

    Reconstructs its own ``env`` from ``variant_make`` rather than receiving a
    live one, since that keeps the pickled task payload small and avoids
    relying on env-pickling semantics we haven't exercised across processes.
    """
    variant_make, control, baseline, baseline_params, env_seed, rng_seed = task
    env = pcg_benchmark.make(variant_make)
    env.seed(env_seed)
    rng = np.random.default_rng(rng_seed)
    if baseline == "wfc":
        content, _ = wfc.generate_content(env, control, rng=rng, **baseline_params)
    elif baseline == "noise":
        content = env.content_space.sample()
    else:
        content, _ = genetic.evolve_content(env, control, rng=rng, **baseline_params)
    return content


def build_baseline_tasks(variant_state, baseline, baseline_params, seed):
    """Flatten every variant's controls into one list of baseline worker tasks.

    Each task gets its own pair of RNG child seeds spawned from a single root
    ``SeedSequence(seed)``, in a fixed (variant order, control index) order --
    this keeps every task's random stream independent (unlike reusing one
    mutating ``Generator`` across sequential calls, which breaks under
    parallel execution) while staying reproducible for a given ``seed``
    regardless of which task happens to finish first.

    Returns ``(tasks, task_meta)`` where ``task_meta[i]`` is the
    ``(variant_key, index_within_variant)`` that ``tasks[i]`` belongs to, so
    results can be regrouped back in ``controls`` order.
    """
    seed_seq = np.random.SeedSequence(seed)
    tasks = []
    task_meta = []
    for variant in VARIANTS:
        state = variant_state.get(variant.key)
        if state is None:
            continue
        for index, control in enumerate(state["controls"]):
            env_seed, rng_seed = seed_seq.spawn(2)
            tasks.append((variant.make, control, baseline, baseline_params, env_seed, rng_seed))
            task_meta.append((variant.key, index))
    return tasks, task_meta


def run_baselines(tasks, task_meta, variant_state, baseline, workers=None):
    """Run every baseline task across a process pool and regroup results by variant.

    Returns ``{variant_key: [content, ...]}`` with each list in the same
    order as ``variant_state[key]["controls"]``.
    """
    pcg_by_variant = {
        key: [None] * len(state["controls"]) for key, state in variant_state.items()
    }
    if not tasks:
        return pcg_by_variant

    total = len(tasks)
    done = 0
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_baseline_worker, task): meta for task, meta in zip(tasks, task_meta)}
        for future in as_completed(futures):
            key, index = futures[future]
            pcg_by_variant[key][index] = future.result()
            done += 1
            if done % 10 == 0 or done == total:
                print(f"{baseline.upper()} baselines: {done}/{total} complete")
    return pcg_by_variant


def evaluate_variant(env, llm_contents, controls, pcg_contents):
    """Evaluate the LLM maps and a same-size GA baseline for one variant.

    Returns the per-variant result dict, matching the historical
    ``eval_results.json`` shape. Caller only invokes this for variants that
    have LLM content (see ``main``'s pass 1).
    """
    quality, diversity, controlability, details, infos = env.evaluate(llm_contents, controls)
    (pcg_quality, pcg_diversity, pcg_controlability,
     pcg_details, pcg_infos) = env.evaluate(pcg_contents, controls)

    result = {
        "quality": quality,
        "diversity": diversity,
        "controlability": controlability,
        "details": details,
        "infos": infos,
        "pcg_quality": pcg_quality,
        "pcg_diversity": pcg_diversity,
        "pcg_controlability": pcg_controlability,
        "pcg_details": pcg_details,
        "pcg_infos": pcg_infos,
    }
    return to_jsonable(result), pcg_contents


def render_maps(env, contents, output_dir, key, method):
    """Render a list of maps to ``{key}_{method}_{i}.png`` in ``output_dir``."""
    if not contents:
        return
    try:
        images = env.render(contents)
    except Exception as exc:  # noqa: BLE001 - one bad batch shouldn't abort the run
        print(f"Failed to render {key} ({method}): {exc}")
        return
    for i, image in enumerate(images):
        try:
            image.save(os.path.join(output_dir, f"{key}_{method}_{i}.png"))
        except Exception as exc:  # noqa: BLE001
            print(f"Failed to save {key}_{method}_{i}.png: {exc}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", default=os.path.join("..", "pcg_results.json"),
                        help="Path to the pcg_results.json with the LLM output.")
    parser.add_argument("--iteration", default=None,
                        help="Iteration number; writes to the results page repo's "
                             "Iterations/<N> folder. Overrides --output-dir.")
    parser.add_argument("--output-dir", default=".",
                        help="Directory to write eval_results.json and PNGs into.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Seed for the random baseline (for reproducible runs).")
    parser.add_argument("--workers", type=int, default=None,
                        help="Worker processes for baseline generation (default: os.cpu_count()).")
    parser.add_argument("--baseline", choices=["noise", "ga", "wfc"], default="ga",
                        help="Non-LLM baseline generator: 'noise' (bare "
                             "env.content_space.sample(), no evolution or synthesis), "
                             "'ga' (genetic.evolve_content), or "
                             "'wfc' (wfc.generate_content, Wave Function Collapse). "
                             "See ../ALGORITHM_RESEARCH.md for the WFC write-up.")
    parser.add_argument("--wfc-rules", choices=["learned", "hand"], default="learned",
                        help="[wfc] Where WFC's adjacency table comes from: 'learned' "
                             "(default -- extracted from a GA-evolved example corpus) or "
                             "'hand' (hand-authored per-problem rules in wfc_rules.py, "
                             "not dependent on example quality -- not yet defined for "
                             "every problem, see wfc_rules.RULES).")
    parser.add_argument("--population-size", type=int, default=genetic.POPULATION_SIZE,
                        help="[ga] GA population size used to build the non-LLM baseline per map.")
    parser.add_argument("--generations", type=int, default=genetic.GENERATIONS,
                        help="[ga] GA generation budget used to build the non-LLM baseline per map.")
    parser.add_argument("--crossover-rate", type=float, default=genetic.CROSSOVER_RATE,
                        help="[ga] Probability of producing a child via crossover instead of cloning.")
    parser.add_argument("--mutation-rate", type=float, default=genetic.MUTATION_RATE,
                        help="[ga/wfc] Per-gene mutation probability (GA evolution, and WFC's own "
                             "post-synthesis polish pass both use this).")
    parser.add_argument("--elite-count", type=int, default=genetic.ELITE_COUNT,
                        help="[ga] Number of top individuals carried over unchanged each generation.")
    parser.add_argument("--tournament-size", type=int, default=genetic.TOURNAMENT_SIZE,
                        help="[ga] Number of individuals sampled per tournament selection.")
    parser.add_argument("--polish-iterations", type=int, default=genetic.POLISH_ITERATIONS,
                        help="[ga] Hill-climb steps applied to the best individual after evolution "
                             "(the wfc baseline has its own --wfc-polish-iterations instead).")
    parser.add_argument("--wfc-corpus-size", type=int, default=wfc.CORPUS_SIZE,
                        help="[wfc] Number of GA-evolved example maps to learn adjacency rules from.")
    parser.add_argument("--wfc-corpus-population", type=int, default=wfc.CORPUS_POPULATION,
                        help="[wfc] GA population size used only to build the example corpus.")
    parser.add_argument("--wfc-corpus-generations", type=int, default=wfc.CORPUS_GENERATIONS,
                        help="[wfc] GA generation budget used only to build the example corpus.")
    parser.add_argument("--wfc-corpus-polish-iterations", type=int, default=wfc.CORPUS_POLISH_ITERATIONS,
                        help="[wfc] GA polish steps used only to build the example corpus.")
    parser.add_argument("--wfc-corpus-elite-count", type=int, default=wfc.CORPUS_ELITE_COUNT,
                        help="[wfc] GA elite count used only to build the example corpus.")
    parser.add_argument("--wfc-max-restarts", type=int, default=wfc.MAX_RESTARTS,
                        help="[wfc] Collapse/propagate attempts before falling back to a "
                             "contradiction-tolerant final pass.")
    parser.add_argument("--wfc-polish-iterations", type=int, default=wfc.POLISH_ITERATIONS,
                        help="[wfc] Hill-climb steps applied to the synthesized map (independent "
                             "of --polish-iterations, which only applies to the ga baseline).")
    args = parser.parse_args()

    if args.iteration is not None:
        args.output_dir = publish.iteration_dir(args.iteration)
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"Writing output to {os.path.abspath(args.output_dir)}")

    llm_contents = parse_results(args.results)
    if not any(llm_contents.values()):
        raise ValueError("No content to evaluate.")

    if args.baseline == "wfc":
        baseline_params = {
            "rules": "auto" if args.wfc_rules == "hand" else None,
            "corpus_size": args.wfc_corpus_size,
            "corpus_population": args.wfc_corpus_population,
            "corpus_generations": args.wfc_corpus_generations,
            "corpus_polish_iterations": args.wfc_corpus_polish_iterations,
            "corpus_elite_count": args.wfc_corpus_elite_count,
            "max_restarts": args.wfc_max_restarts,
            "polish_iterations": args.wfc_polish_iterations,
            "mutation_rate": args.mutation_rate,
        }
    elif args.baseline == "noise":
        baseline_params = {}
    else:
        baseline_params = {
            "population_size": args.population_size,
            "generations": args.generations,
            "crossover_rate": args.crossover_rate,
            "mutation_rate": args.mutation_rate,
            "elite_count": args.elite_count,
            "tournament_size": args.tournament_size,
            "polish_iterations": args.polish_iterations,
        }

    # Pass 1: build each variant's env and shared controls (cheap, sequential).
    variant_state = {}
    for variant in VARIANTS:
        contents = llm_contents[variant.key]
        if not contents:
            continue

        env = pcg_benchmark.make(variant.make)
        if args.seed is not None:
            env.seed(args.seed)

        controls = [env.control_space.sample() for _ in range(len(contents))]
        variant_state[variant.key] = {"env": env, "contents": contents, "controls": controls}

    # Pass 2: generate every (variant, control) baseline across a process
    # pool -- flattened across all variants so low-count variants don't
    # leave workers idle (see runner.py module docstring / RUNNER.md).
    tasks, task_meta = build_baseline_tasks(variant_state, args.baseline, baseline_params, args.seed)
    pcg_by_variant = run_baselines(tasks, task_meta, variant_state, args.baseline, workers=args.workers)

    # Pass 3: evaluate + render (unchanged apart from getting pcg_contents
    # from the pool instead of computing it inline).
    eval_results = {}
    for variant in VARIANTS:
        state = variant_state.get(variant.key)
        if state is None:
            continue
        env, contents, controls = state["env"], state["contents"], state["controls"]
        pcg_contents = pcg_by_variant[variant.key]

        result, pcg_contents = evaluate_variant(env, contents, controls, pcg_contents)
        eval_results[variant.key] = result

        render_maps(env, contents, args.output_dir, variant.key, "llm")
        render_maps(env, pcg_contents, args.output_dir, variant.key, "pcg")
        print(f"Evaluated {variant.key}: {len(contents)} maps")

    out_path = os.path.join(args.output_dir, "eval_results.json")
    with open(out_path, "w") as f:
        json.dump(eval_results, f, indent=4)
    print(f"Wrote {out_path}")

    config_path = os.path.join(args.output_dir, "run_config.json")
    with open(config_path, "w") as f:
        json.dump({"baseline": args.baseline, **vars(args)}, f, indent=4)
    print(f"Wrote {config_path}")


if __name__ == "__main__":
    main()
