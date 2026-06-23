"""Turn an iteration's ``eval_results.json`` into comparison tables.

The benchmark scores both methods (LLM and the random non-LLM baseline) on
three metrics:

  * quality        - fraction of maps that are valid / playable,
  * diversity       - fraction of maps that are sufficiently different,
  * controlability  - fraction of maps that hit the requested control targets.

This module loads those results with pandas and produces:

  * a *per-map* table (raw detail scores, one row per map) -> ``analysis.csv``
  * a *per-variant summary* (aggregate score per method + deltas + winner)
    -> ``summary.csv``
  * a ``compare()`` verdict that says which method wins overall.

It is imported by ``report.py`` and can also be run standalone on a folder.
"""

import json
import os

import pandas as pd

from variants import VARIANTS

METRICS = ["quality", "diversity", "controlability"]
METHODS = {"llm": "LLM", "pcg": "Non-LLM"}


def load_iteration(folder: str) -> dict:
    """Read ``eval_results.json`` from an iteration folder."""
    with open(os.path.join(folder, "eval_results.json"), "r") as f:
        return json.load(f)


def _details_key(method: str) -> str:
    """Map a method to its details key in eval_results.json."""
    return "details" if method == "llm" else "pcg_details"


def _metric_mean(result: dict, method: str, metric: str) -> float:
    """Average the per-map scores for a metric from the details section.

    The top-level ``quality``/``diversity``/``controlability`` aggregates can be
    off, so we compute the mean directly from the per-map arrays under
    ``details`` (LLM) / ``pcg_details`` (non-LLM).
    """
    details = result.get(_details_key(method)) or {}
    values = details.get(metric, [])
    return float(sum(values) / len(values)) if values else 0.0


def build_per_map_df(data: dict) -> pd.DataFrame:
    """One row per (variant, method, map_index) with detail scores.

    Pulls the per-map arrays out of ``details`` / ``pcg_details``.
    """
    rows = []
    known = {v.key: v.label for v in VARIANTS}
    for key, result in data.items():
        label = known.get(key, key)
        for method, method_label in METHODS.items():
            details_key = "details" if method == "llm" else "pcg_details"
            details = result.get(details_key) or {}
            per_metric = {m: details.get(m, []) for m in METRICS}
            count = max((len(v) for v in per_metric.values()), default=0)
            for i in range(count):
                row = {"variant": key, "label": label, "method": method_label, "map_index": i}
                for metric in METRICS:
                    values = per_metric[metric]
                    row[metric] = values[i] if i < len(values) else None
                rows.append(row)
    return pd.DataFrame(rows, columns=["variant", "label", "method", "map_index", *METRICS])


def build_summary_df(data: dict) -> pd.DataFrame:
    """One row per variant with aggregate LLM vs non-LLM scores and winners."""
    rows = []
    known = {v.key: v.label for v in VARIANTS}
    for key, result in data.items():
        row = {"variant": key, "label": known.get(key, key)}
        for metric in METRICS:
            llm = _metric_mean(result, "llm", metric)
            pcg = _metric_mean(result, "pcg", metric)
            row[f"llm_{metric}"] = llm
            row[f"pcg_{metric}"] = pcg
            row[f"delta_{metric}"] = llm - pcg
            if llm > pcg:
                row[f"winner_{metric}"] = "LLM"
            elif pcg > llm:
                row[f"winner_{metric}"] = "Non-LLM"
            else:
                row[f"winner_{metric}"] = "Tie"
        rows.append(row)
    columns = ["variant", "label"]
    for metric in METRICS:
        columns += [f"llm_{metric}", f"pcg_{metric}", f"delta_{metric}", f"winner_{metric}"]
    return pd.DataFrame(rows, columns=columns)


def compare(summary: pd.DataFrame) -> dict:
    """Aggregate the per-variant summary into an overall verdict.

    Returns per-metric means (LLM vs non-LLM), the delta, how many variants
    each method wins, and an overall verdict.
    """
    result = {"metrics": {}, "n_variants": int(len(summary))}
    metric_winners = []
    for metric in METRICS:
        llm_mean = float(summary[f"llm_{metric}"].mean()) if len(summary) else 0.0
        pcg_mean = float(summary[f"pcg_{metric}"].mean()) if len(summary) else 0.0
        wins = summary[f"winner_{metric}"].value_counts().to_dict()
        if llm_mean > pcg_mean:
            metric_winner = "LLM"
        elif pcg_mean > llm_mean:
            metric_winner = "Non-LLM"
        else:
            metric_winner = "Tie"
        metric_winners.append(metric_winner)
        result["metrics"][metric] = {
            "llm_mean": llm_mean,
            "pcg_mean": pcg_mean,
            "delta": llm_mean - pcg_mean,
            "llm_wins": int(wins.get("LLM", 0)),
            "pcg_wins": int(wins.get("Non-LLM", 0)),
            "ties": int(wins.get("Tie", 0)),
            "winner": metric_winner,
        }
    llm_metrics = metric_winners.count("LLM")
    pcg_metrics = metric_winners.count("Non-LLM")
    if llm_metrics > pcg_metrics:
        result["overall"] = "LLM"
    elif pcg_metrics > llm_metrics:
        result["overall"] = "Non-LLM"
    else:
        result["overall"] = "Tie"
    return result


def write_csvs(folder: str):
    """Convenience: load a folder and write both CSVs into it. Returns frames."""
    data = load_iteration(folder)
    per_map = build_per_map_df(data)
    summary = build_summary_df(data)
    per_map.to_csv(os.path.join(folder, "analysis.csv"), index=False)
    summary.to_csv(os.path.join(folder, "summary.csv"), index=False)
    return per_map, summary, compare(summary)


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "."
    _, summary_df, verdict = write_csvs(target)
    print(summary_df.to_string(index=False))
    print()
    print(f"Overall winner: {verdict['overall']}")
