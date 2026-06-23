"""Single source of truth for the benchmark variants.

Every game variant is identical in shape; it differs only by three strings:

  key         - identifier used in ``eval_results.json`` and in PNG file names
                (e.g. ``binary_v0``).
  make        - name passed to ``pcg_benchmark.make(...)`` (e.g. ``binary-v0``).
  json_prefix - prefix of the keys in ``pcg_results.json`` under
                ``data["Output"]``; each map is stored as ``"{json_prefix}-{i}"``.
                Note this can differ from ``make`` (e.g. mario vs smbtile).

``runner.py`` (evaluation) and ``report.py`` (reporting) both import this list so
they can never drift out of sync.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Variant:
    key: str
    make: str
    json_prefix: str

    @property
    def label(self) -> str:
        """Human readable name, e.g. ``binary_v0`` -> ``Binary V0``."""
        return self.key.replace("_", " ").title()


VARIANTS = [
    Variant("binary_v0", "binary-v0", "binary-v0"),
    Variant("binary_large_v0", "binary-large-v0", "binary-large-v0"),
    Variant("binary_wide_v0", "binary-wide-v0", "binary-wide-v0"),
    Variant("ddave_v0", "ddave-v0", "ddave-v0"),
    Variant("ddave_complex_v0", "ddave-complex-v0", "ddave-complex-v0"),
    Variant("ddave_large_v0", "ddave-large-v0", "ddave-large-v0"),
    Variant("loderunner_v0", "loderunnertile-v0", "loderunner-v0"),
    Variant("loderunner_gold_v0", "loderunnertile-gold-v0", "loderunner-gold-v0"),
    Variant("loderunner_enemies_v0", "loderunnertile-enemies-v0", "loderunner-enemies-v0"),
    Variant("mdungeons_v0", "mdungeons-v0", "mdungeons-v0"),
    Variant("mdungeons_large_v0", "mdungeons-large-v0", "mdungeons-large-v0"),
    Variant("mdungeons_enemies_v0", "mdungeons-enemies-v0", "mdungeons-enemies-v0"),
    Variant("sokoban_v0", "sokoban-v0", "sokoban-v0"),
    Variant("sokoban_large_v0", "sokoban-large-v0", "sokoban-large-v0"),
    Variant("sokoban_complex_v0", "sokoban-complex-v0", "sokoban-complex-v0"),
    Variant("smbtile_v0", "smbtile-v0", "mario-v0"),
    Variant("smbtile_medium_v0", "smbtile-medium-v0", "mario-medium-v0"),
    Variant("smbtile_small_v0", "smbtile-small-v0", "mario-small-v0"),
    Variant("zelda_v0", "zelda-v0", "zelda-v0"),
    Variant("zelda_enemies_v0", "zelda-enemies-v0", "zelda-enemies-v0"),
    Variant("zelda_large_v0", "zelda-large-v0", "zelda-large-v0"),
]

# Lookup of json_prefix -> Variant, used when bucketing the LLM results.
VARIANTS_BY_PREFIX = {v.json_prefix: v for v in VARIANTS}
