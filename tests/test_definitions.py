"""Pin the emitted taxonomy shape and the hand-transcribed values.

Every table here is a literal, written independently of `definitions.py`, so a
mistyped motif or a mistagged `liabilityType` fails here rather than in a
consuming block.
"""

import json
import re

import pytest

import main
from definitions import FIXABILITY_WEIGHTS, LIABILITIES, SCHEMA_VERSION

ENTRY_KEYS = {"id", "name", "liabilityType", "motif", "riskLevel", "fixability"}

FIXABILITY_CLASSES = {
    "easily_fixable",
    "fixable",
    "hard_to_fix",
    "structural",
    "disqualifying",
}

RISK_LEVELS = {"Low", "Medium", "High"}

LIABILITY_TYPES = {
    "deamidation",
    "isomerization",
    "fragmentation",
    "glycosylation",
    "hydrolysis",
    "oxidation",
    "cysteine",
    "integrin",
    "sequence-artifact",
}

# name -> liabilityType, for all fifteen definitions.
EXPECTED_TYPE_BY_NAME = {
    "Deamidation (N[GS])": "deamidation",
    "Fragmentation (DP)": "fragmentation",
    "Isomerization (D[DGHST])": "isomerization",
    "N-linked Glycosylation (N[^P][ST])": "glycosylation",
    "Deamidation (N[AHNT])": "deamidation",
    "Hydrolysis (NP)": "hydrolysis",
    "Fragmentation (TS)": "fragmentation",
    "Tryptophan Oxidation (W)": "oxidation",
    "Methionine Oxidation (M)": "oxidation",
    "Deamidation ([STK]N)": "deamidation",
    "Integrin binding": "integrin",
    "Contains stop codon": "sequence-artifact",
    "Out of frame": "sequence-artifact",
    "Missing Cysteines": "cysteine",
    "Extra Cysteines": "cysteine",
}

# name -> (motif, riskLevel, fixability), transcribed from
# antibody-sequence-liabilities/liabilities-calc-script/src/definitions.py
# ORIG_REGEX_LIABILITIES.
EXPECTED_REGEX_ENTRIES = {
    "Deamidation (N[GS])": (r"N[GS]", "High", "fixable"),
    "Fragmentation (DP)": (r"DP", "High", "fixable"),
    "Isomerization (D[DGHST])": (r"D[DGHST]", "High", "fixable"),
    "N-linked Glycosylation (N[^P][ST])": (r"N[^P][ST]", "High", "fixable"),
    "Deamidation (N[AHNT])": (r"N[AHNT]", "Medium", "easily_fixable"),
    "Hydrolysis (NP)": (r"NP", "Medium", "fixable"),
    "Fragmentation (TS)": (r"TS", "Medium", "fixable"),
    "Tryptophan Oxidation (W)": (r"W", "Medium", "easily_fixable"),
    "Methionine Oxidation (M)": (r"M", "Medium", "easily_fixable"),
    "Deamidation ([STK]N)": (r"[STK]N", "Low", "easily_fixable"),
    "Integrin binding": (r"RGD|RYD|KGD|NGR|LDV|DGE|GPR", "Low", "easily_fixable"),
}

# The four entries that are not in ORIG_REGEX_LIABILITIES: the two
# sequence-artifact patterns (always disqualifying) and the two cysteine-state
# liabilities, whose detection is a count against expected positions, not a
# motif match — so their motif is None.
EXPECTED_NON_REGEX_ENTRIES = {
    "Contains stop codon": (r"\*", "High", "disqualifying"),
    "Out of frame": (r"_", "High", "disqualifying"),
    "Missing Cysteines": (None, "High", "structural"),
    "Extra Cysteines": (None, "High", "hard_to_fix"),
}


def _by_name() -> dict[str, dict]:
    return {entry["name"]: entry for entry in LIABILITIES}


def test_fifteen_definitions_with_unique_ids():
    assert len(LIABILITIES) == 15
    ids = [entry["id"] for entry in LIABILITIES]
    assert len(set(ids)) == 15
    names = [entry["name"] for entry in LIABILITIES]
    assert len(set(names)) == 15


def test_every_entry_has_exactly_the_six_fields():
    for entry in LIABILITIES:
        assert set(entry) == ENTRY_KEYS, entry


def test_fixability_values_are_weightable():
    for entry in LIABILITIES:
        assert entry["fixability"] in FIXABILITY_CLASSES, entry
    assert set(FIXABILITY_WEIGHTS) == FIXABILITY_CLASSES


def test_risk_levels_are_in_the_closed_set():
    for entry in LIABILITIES:
        assert entry["riskLevel"] in RISK_LEVELS, entry


def test_liability_types_match_the_pinned_name_to_type_table():
    for entry in LIABILITIES:
        assert entry["liabilityType"] in LIABILITY_TYPES, entry
    actual = {entry["name"]: entry["liabilityType"] for entry in LIABILITIES}
    assert actual == EXPECTED_TYPE_BY_NAME


def test_regex_entries_match_the_transcribed_values():
    entries = _by_name()
    actual = {
        name: (entries[name]["motif"], entries[name]["riskLevel"], entries[name]["fixability"])
        for name in EXPECTED_REGEX_ENTRIES
    }
    assert actual == EXPECTED_REGEX_ENTRIES


def test_non_regex_entries_match_the_transcribed_values():
    entries = _by_name()
    actual = {
        name: (entries[name]["motif"], entries[name]["riskLevel"], entries[name]["fixability"])
        for name in EXPECTED_NON_REGEX_ENTRIES
    }
    assert actual == EXPECTED_NON_REGEX_ENTRIES


def test_only_the_cysteine_state_liabilities_carry_no_motif():
    motifless = [entry for entry in LIABILITIES if entry["motif"] is None]
    assert len(motifless) == 2
    assert {entry["liabilityType"] for entry in motifless} == {"cysteine"}


def test_every_motif_compiles():
    for entry in LIABILITIES:
        if entry["motif"] is None:
            continue
        re.compile(entry["motif"])


def test_emitter_writes_the_three_key_document(tmp_path, monkeypatch):
    out = tmp_path / "taxonomy.json"
    monkeypatch.setattr("sys.argv", ["main.py", str(out)])
    main.main()

    document = json.loads(out.read_text(encoding="utf-8"))
    assert set(document) == {"schemaVersion", "liabilities", "fixabilityWeights"}
    assert document["schemaVersion"] == SCHEMA_VERSION
    assert len(document["liabilities"]) == 15
    assert document["fixabilityWeights"] == FIXABILITY_WEIGHTS


def test_emitter_refuses_an_empty_taxonomy(tmp_path, monkeypatch):
    out = tmp_path / "taxonomy.json"
    monkeypatch.setattr(main, "LIABILITIES", [])
    monkeypatch.setattr("sys.argv", ["main.py", str(out)])

    with pytest.raises(SystemExit):
        main.main()
    assert not out.exists()
