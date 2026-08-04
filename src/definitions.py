"""The canonical liability taxonomy. NOT POPULATED YET.

Fill from the two verbatim copies this package replaces, which must then read
this package instead of their own literal:

  antibody-sequence-liabilities/liabilities-calc-script/src/definitions.py
  3D-Structure-Based-Liabilities/software/liabilities-script/motifs.py

Every entry is one `Liability` definition. `fixability` decides which
liabilities the variant designer will try to repair; `easily_fixable` and
`fixable` generate variants, `hard_to_fix` is annotate-only, and `structural`
and `disqualifying` never generate.

`SCHEMA_VERSION` is bumped whenever a field is added or a field's meaning
changes, so a consumer can refuse a taxonomy it does not understand. Room is
left for a canonical-substitution table, deferred out of V0.5.
"""

SCHEMA_VERSION = 1

# One dict per liability: id, name, motif (regex), riskLevel, fixability.
LIABILITIES: list[dict] = []

# Fixability class -> weight, as used by the developability cost.
FIXABILITY_WEIGHTS: dict[str, float] = {}
