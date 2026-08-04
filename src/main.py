#!/usr/bin/env python
"""Emit the canonical antibody liability taxonomy as JSON.

Definitions only — never a scan. The three consuming blocks scan differently
(sequence-only, SASA-and-confidence-gated, and the variant designer's rescan
that must keep buried hits), so a shared scan would force those behaviours
into one function.

The emitted vocabulary is `liabilities`, not `motifHits`: this file fixes the
terms for every consumer.
"""

import argparse
import json

from definitions import FIXABILITY_WEIGHTS, LIABILITIES, SCHEMA_VERSION


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write the canonical liability taxonomy as JSON")
    parser.add_argument("output", help="output json file")
    args = parser.parse_args()

    if not LIABILITIES or not FIXABILITY_WEIGHTS:
        raise SystemExit(
            "liability taxonomy is empty — populate src/definitions.py before "
            "publishing this package; see README.md")

    taxonomy = {
        "schemaVersion": SCHEMA_VERSION,
        "liabilities": LIABILITIES,
        "fixabilityWeights": FIXABILITY_WEIGHTS,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(taxonomy, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
