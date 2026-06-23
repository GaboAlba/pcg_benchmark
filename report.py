"""Build a static HTML report comparing LLM vs non-LLM level generation.

Walks the ``Iterations`` folder. Each numbered sub-folder holds one run's
``eval_results.json`` (and the rendered map PNGs). For every iteration this:

  * writes ``analysis.csv`` + ``summary.csv`` (raw data for deeper digging),
  * renders matplotlib comparison charts,
  * writes an iteration page (``index.html``) with the verdict, the comparison
    tables, the charts, and a side-by-side LLM vs non-LLM map gallery.

Per the agreed workflow, an iteration page is only generated if it does not
already exist (so finished iterations are never rebuilt). The home page is
always regenerated so newly added iterations show up.

Usage:
    python report.py [--iterations DIR] [--force]
"""

import argparse
import glob
import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import analysis
from analysis import METRICS
from variants import VARIANTS

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ITERATIONS = os.path.normpath(os.path.join(HERE, "..", "Iterations"))
CONTROL_FILE = "Iteration Control.txt"

STYLE = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
       margin: 0; color: #1f2933; background: #f5f7fa; line-height: 1.5; }
.container { max-width: 1100px; margin: 0 auto; padding: 32px 24px 80px; }
h1 { font-size: 28px; margin: 0 0 4px; }
h2 { font-size: 21px; margin: 40px 0 12px; border-bottom: 2px solid #e4e7eb; padding-bottom: 6px; }
h3 { font-size: 16px; margin: 28px 0 8px; }
a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }
.subtitle { color: #616e7c; margin: 0 0 24px; }
.verdict { display: inline-block; padding: 10px 18px; border-radius: 8px; font-weight: 600;
           background: #e8f0fe; color: #1a3e8c; margin: 8px 0 16px; }
.verdict.llm { background: #e6f4ea; color: #1e7d34; }
.verdict.pcg { background: #fdeceb; color: #b3261e; }
.verdict.tie { background: #f3f0e6; color: #8a6d1f; }
table { border-collapse: collapse; width: 100%; font-size: 13px; background: #fff;
        box-shadow: 0 1px 2px rgba(0,0,0,.06); border-radius: 8px; overflow: hidden; }
th, td { padding: 8px 10px; text-align: right; border-bottom: 1px solid #eef1f4; }
th:first-child, td:first-child { text-align: left; }
thead th { background: #1f2933; color: #fff; font-weight: 600; }
tbody tr:hover { background: #f8fafc; }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.card { background: #fff; border-radius: 10px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,.08);
        display: block; }
.card h3 { margin: 0 0 6px; }
img.chart { max-width: 100%; background: #fff; border-radius: 8px; padding: 8px;
            box-shadow: 0 1px 2px rgba(0,0,0,.06); margin: 8px 0; }
.gallery { margin: 8px 0 24px; }
.gallery .row { display: flex; gap: 24px; flex-wrap: wrap; }
.gallery .col { flex: 1 1 360px; }
.gallery .strip { display: flex; flex-wrap: wrap; gap: 4px; }
.gallery .strip img { height: 72px; image-rendering: pixelated; border: 1px solid #d2d6dc;
                      background: #fff; border-radius: 2px; }
.method-label { font-weight: 600; font-size: 13px; margin: 4px 0; color: #3e4c59; }
.muted { color: #9aa5b1; font-size: 13px; }
"""


def parse_control_file(iterations_root: str) -> dict:
    """Parse ``Iteration Control.txt`` -> {index(str): description}."""
    path = os.path.join(iterations_root, CONTROL_FILE)
    titles = {}
    if not os.path.exists(path):
        return titles
    with open(path, "r") as f:
        for line in f:
            if ":" in line:
                idx, desc = line.split(":", 1)
                titles[idx.strip()] = desc.strip()
    return titles


def find_iteration_dirs(iterations_root: str) -> "list[tuple[str, str]]":
    """Return sorted ``(name, path)`` for numeric sub-folders with results."""
    found = []
    for name in os.listdir(iterations_root):
        path = os.path.join(iterations_root, name)
        if name.isdigit() and os.path.isdir(path) and \
                os.path.exists(os.path.join(path, "eval_results.json")):
            found.append((name, path))
    found.sort(key=lambda item: int(item[0]))
    return found


def _verdict_class(winner: str) -> str:
    return {"LLM": "llm", "Non-LLM": "pcg"}.get(winner, "tie")


def collect_gallery_images(folder: str, key: str) -> "tuple[list[str], list[str]]":
    """Find rendered maps for a variant, returning (llm_files, pcg_files).

    Prefers the new ``{key}_llm_*`` / ``{key}_pcg_*`` naming. Falls back to the
    legacy ``{key}_{i}.png`` (LLM only) used by older iterations.
    """
    def sorted_glob(pattern):
        files = glob.glob(os.path.join(folder, pattern))
        files.sort(key=lambda p: int(re.search(r"_(\d+)\.png$", p).group(1))
                   if re.search(r"_(\d+)\.png$", p) else 0)
        return [os.path.basename(p) for p in files]

    llm = sorted_glob(f"{key}_llm_*.png")
    pcg = sorted_glob(f"{key}_pcg_*.png")
    if not llm and not pcg:
        legacy = glob.glob(os.path.join(folder, f"{key}_*.png"))
        # Exclude chart images that happen to start with the key (none do, but be safe).
        legacy = [p for p in legacy if re.search(rf"{re.escape(key)}_\d+\.png$", os.path.basename(p))]
        legacy.sort(key=lambda p: int(re.search(r"_(\d+)\.png$", p).group(1)))
        llm = [os.path.basename(p) for p in legacy]
    return llm, pcg


def make_charts(folder: str, summary, verdict: dict):
    """Render comparison charts as PNGs into the iteration folder."""
    # Overall means: grouped bars, 3 metrics x 2 methods.
    metrics = METRICS
    llm_means = [verdict["metrics"][m]["llm_mean"] for m in metrics]
    pcg_means = [verdict["metrics"][m]["pcg_mean"] for m in metrics]
    x = np.arange(len(metrics))
    width = 0.38
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(x - width / 2, llm_means, width, label="LLM", color="#2563eb")
    ax.bar(x + width / 2, pcg_means, width, label="Non-LLM", color="#9aa5b1")
    ax.set_xticks(x)
    ax.set_xticklabels([m.capitalize() for m in metrics])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Mean score (across variants)")
    ax.set_title("LLM vs Non-LLM — mean per metric")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(folder, "chart_overall.png"), dpi=110)
    plt.close(fig)

    # Per-variant grouped horizontal bars, one chart per metric.
    labels = summary["label"].tolist()
    y = np.arange(len(labels))
    height = max(3.0, 0.42 * len(labels))
    for metric in metrics:
        fig, ax = plt.subplots(figsize=(8, height))
        ax.barh(y - width / 2, summary[f"llm_{metric}"], width, label="LLM", color="#2563eb")
        ax.barh(y + width / 2, summary[f"pcg_{metric}"], width, label="Non-LLM", color="#9aa5b1")
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=8)
        ax.invert_yaxis()
        ax.set_xlim(0, 1)
        ax.set_xlabel(f"{metric.capitalize()} score")
        ax.set_title(f"{metric.capitalize()} by variant")
        ax.legend(loc="lower right")
        fig.tight_layout()
        fig.savefig(os.path.join(folder, f"chart_{metric}.png"), dpi=110)
        plt.close(fig)


def _summary_table_html(summary) -> str:
    """Format the summary DataFrame as an HTML table."""
    display = summary.copy()
    display = display.drop(columns=["variant"])
    for col in display.columns:
        if display[col].dtype.kind == "f":
            display[col] = display[col].map(lambda v: f"{v:+.3f}" if col.startswith("delta")
                                            else f"{v:.3f}")
    rename = {"label": "Variant"}
    for m in METRICS:
        rename[f"llm_{m}"] = f"LLM {m[:4]}"
        rename[f"pcg_{m}"] = f"PCG {m[:4]}"
        rename[f"delta_{m}"] = f"Δ {m[:4]}"
        rename[f"winner_{m}"] = f"Win {m[:4]}"
    display = display.rename(columns=rename)
    return display.to_html(index=False, border=0)


def render_iteration_page(folder, name, title, data, summary, verdict):
    """Write the iteration ``index.html``."""
    metric_rows = "".join(
        f"<tr><td>{m.capitalize()}</td><td>{d['llm_mean']:.3f}</td>"
        f"<td>{d['pcg_mean']:.3f}</td><td>{d['delta']:+.3f}</td>"
        f"<td>{d['llm_wins']}</td><td>{d['pcg_wins']}</td><td>{d['ties']}</td>"
        f"<td>{d['winner']}</td></tr>"
        for m, d in ((m, verdict["metrics"][m]) for m in METRICS)
    )

    galleries = []
    known = {v.key: v.label for v in VARIANTS}
    for key in data.keys():
        llm_files, pcg_files = collect_gallery_images(folder, key)
        if not llm_files and not pcg_files:
            continue
        llm_imgs = "".join(f'<img src="{f}" alt="{f}">' for f in llm_files)
        pcg_imgs = "".join(f'<img src="{f}" alt="{f}">' for f in pcg_files) \
            or '<span class="muted">not rendered for this iteration</span>'
        galleries.append(f"""
        <h3>{known.get(key, key)}</h3>
        <div class="gallery"><div class="row">
          <div class="col"><div class="method-label">LLM</div><div class="strip">{llm_imgs}</div></div>
          <div class="col"><div class="method-label">Non-LLM (random)</div><div class="strip">{pcg_imgs}</div></div>
        </div></div>""")

    overall = verdict["overall"]
    chart_imgs = '<img class="chart" src="chart_overall.png" alt="overall means">'
    for metric in METRICS:
        chart_imgs += f'<img class="chart" src="chart_{metric}.png" alt="{metric} by variant">'

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Iteration {name} — PCG Benchmark</title><style>{STYLE}</style></head>
<body><div class="container">
<p><a href="../index.html">&larr; All iterations</a></p>
<h1>Iteration {name}</h1>
<p class="subtitle">{title}</p>
<div class="verdict {_verdict_class(overall)}">Overall winner: {overall}
&nbsp;·&nbsp; {verdict['n_variants']} variant(s)</div>

<h2>Metric comparison</h2>
<table><thead><tr><th>Metric</th><th>LLM mean</th><th>Non-LLM mean</th><th>Δ</th>
<th>LLM wins</th><th>Non-LLM wins</th><th>Ties</th><th>Winner</th></tr></thead>
<tbody>{metric_rows}</tbody></table>

<h2>Charts</h2>
{chart_imgs}

<h2>Per-variant summary</h2>
{_summary_table_html(summary)}
<p class="muted">Raw data: <a href="analysis.csv">analysis.csv</a> (per map) ·
<a href="summary.csv">summary.csv</a> (per variant) ·
<a href="eval_results.json">eval_results.json</a></p>

<h2>Map gallery</h2>
{''.join(galleries) if galleries else '<p class="muted">No rendered maps found.</p>'}
</div></body></html>"""

    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def render_home(iterations_root, entries):
    """Write the home ``index.html`` with methodology + iteration links."""
    cards = ""
    for name, title, verdict in entries:
        winner = verdict["overall"] if verdict else "—"
        badge = f'<div class="verdict {_verdict_class(winner)}">Winner: {winner}</div>' if verdict else ""
        cards += f"""
        <a class="card" href="{name}/index.html">
          <h3>Iteration {name}</h3>
          <p class="muted">{title}</p>
          {badge}
        </a>"""

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PCG Benchmark — LLM vs Non-LLM</title><style>{STYLE}</style></head>
<body><div class="container">
<h1>PCG Benchmark Report</h1>
<p class="subtitle">Comparing LLM-generated levels against a non-LLM random baseline.</p>

<h2>What is being evaluated</h2>
<p>For each game variant the benchmark takes a set of <strong>LLM-generated</strong>
levels and an equally sized <strong>non-LLM</strong> baseline (levels sampled randomly
from the same content space). Both sets are scored against the same control targets so
the comparison is fair. The goal is to determine which method produces better levels.</p>

<h2>How it is measured</h2>
<p>Every level set is scored on three metrics, each reported as a fraction in [0, 1]
(higher is better):</p>
<table><thead><tr><th>Metric</th><th>Meaning</th></tr></thead><tbody>
<tr><td>Quality</td><td>Fraction of levels that are valid / playable (e.g. solvable,
correctly connected, right number of objects for that game).</td></tr>
<tr><td>Diversity</td><td>Fraction of levels that are sufficiently different from the
others in the set (avoids near-duplicate output).</td></tr>
<tr><td>Controlability</td><td>Fraction of levels that match the requested control
targets (e.g. a target path length or object count).</td></tr>
</tbody></table>
<p>Each iteration aggregates these per variant, declares a winner per metric, and an
overall winner (the method that wins the most metrics). Raw per-map and per-variant
data is exported as CSV next to each iteration for deeper analysis.</p>

<h2>Iterations</h2>
<div class="cards">{cards or '<p class="muted">No iterations found.</p>'}</div>
</div></body></html>"""

    with open(os.path.join(iterations_root, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", default=DEFAULT_ITERATIONS,
                        help="Path to the Iterations folder.")
    parser.add_argument("--force", action="store_true",
                        help="Rebuild iteration pages even if they already exist.")
    args = parser.parse_args()

    root = args.iterations
    titles = parse_control_file(root)
    entries = []

    for name, folder in find_iteration_dirs(root):
        title = titles.get(name, f"Iteration {name}")
        page = os.path.join(folder, "index.html")

        data = analysis.load_iteration(folder)
        summary = analysis.build_summary_df(data)
        verdict = analysis.compare(summary)

        if os.path.exists(page) and not args.force:
            print(f"Iteration {name}: page exists, skipping (use --force to rebuild)")
        else:
            analysis.build_per_map_df(data).to_csv(os.path.join(folder, "analysis.csv"), index=False)
            summary.to_csv(os.path.join(folder, "summary.csv"), index=False)
            make_charts(folder, summary, verdict)
            render_iteration_page(folder, name, title, data, summary, verdict)
            print(f"Iteration {name}: generated")

        entries.append((name, title, verdict))

    render_home(root, entries)
    print(f"Wrote {os.path.join(root, 'index.html')}")


if __name__ == "__main__":
    main()
