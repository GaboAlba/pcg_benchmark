"""Evaluate LLM-generated levels against a random (non-LLM) baseline.

For every variant in ``variants.VARIANTS`` this script:

  1. loads the LLM-generated maps from ``pcg_results.json``,
  2. samples a random baseline of the same size from the content space,
  3. evaluates both with the benchmark (quality / diversity / controlability)
     using a shared set of control targets so the comparison is fair,
  4. writes the combined metrics to ``eval_results.json``, and
  5. renders both the LLM and the baseline maps to PNG files.

The whole thing is driven by the single ``VARIANTS`` table, so adding or
removing a variant is a one-line change in ``variants.py``.

Usage:
    python runner.py [--results PATH] [--output-dir DIR] [--seed N]
"""

import argparse
import json
import os

import numpy as np

import pcg_benchmark
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

    Keys in the results file look like ``"{json_prefix}-{index}"`` (e.g.
    ``"binary-v0-12"``); we split off the trailing index with ``rsplit`` so it
    keeps working for indices >= 10.
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

        prefix = result_key.rsplit("-", 1)[0]
        variant = VARIANTS_BY_PREFIX.get(prefix)
        if variant is None:
            print(f"Unknown content key: {result_key}")
            continue

        contents[variant.key].append(level)

    return contents


def evaluate_variant(env, llm_contents):
    """Evaluate the LLM maps and a same-size random baseline for one variant.

    Returns the per-variant result dict (matching the historical
    ``eval_results.json`` shape) or ``None`` if there were no LLM maps.
    """
    if not llm_contents:
        return None

    count = len(llm_contents)
    pcg_contents = [env.content_space.sample() for _ in range(count)]
    # Shared controls applied to BOTH methods so controlability is comparable.
    controls = [env.control_space.sample() for _ in range(count)]

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
    parser.add_argument("--output-dir", default=".",
                        help="Directory to write eval_results.json and PNGs into.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Seed for the random baseline (for reproducible runs).")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    llm_contents = parse_results(args.results)
    if not any(llm_contents.values()):
        raise ValueError("No content to evaluate.")

    eval_results = {}
    for variant in VARIANTS:
        contents = llm_contents[variant.key]
        if not contents:
            continue

        env = pcg_benchmark.make(variant.make)
        if args.seed is not None:
            env.seed(args.seed)

        outcome = evaluate_variant(env, contents)
        if outcome is None:
            continue
        result, pcg_contents = outcome
        eval_results[variant.key] = result

        render_maps(env, contents, args.output_dir, variant.key, "llm")
        render_maps(env, pcg_contents, args.output_dir, variant.key, "pcg")
        print(f"Evaluated {variant.key}: {len(contents)} maps")

    out_path = os.path.join(args.output_dir, "eval_results.json")
    with open(out_path, "w") as f:
        json.dump(eval_results, f, indent=4)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
