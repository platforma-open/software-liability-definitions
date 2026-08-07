"""The canonical liability taxonomy. Definitions only, never a scan."""

SCHEMA_VERSION = 1

# One dict per Liability definition.
#   id            stable snake_case key, safe to use as a dict key or column suffix
#   name          the display spelling every shipped block already uses — do not reword
#   liabilityType closed set: deamidation | isomerization | fragmentation | glycosylation
#                 | hydrolysis | oxidation | cysteine | integrin | sequence-artifact
#   motif         regex over one-letter residues, or None when detection is not a motif match
#   riskLevel     Low | Medium | High
#   fixability    easily_fixable | fixable | hard_to_fix | structural | disqualifying
LIABILITIES: list[dict] = [
    {"id": "deamidation_ng", "name": "Deamidation (N[GS])",
     "liabilityType": "deamidation", "motif": r"N[GS]",
     "riskLevel": "High", "fixability": "fixable"},
    {"id": "fragmentation_dp", "name": "Fragmentation (DP)",
     "liabilityType": "fragmentation", "motif": r"DP",
     "riskLevel": "High", "fixability": "fixable"},
    {"id": "isomerization_ddghst", "name": "Isomerization (D[DGHST])",
     "liabilityType": "isomerization", "motif": r"D[DGHST]",
     "riskLevel": "High", "fixability": "fixable"},
    {"id": "n_linked_glycosylation", "name": "N-linked Glycosylation (N[^P][ST])",
     "liabilityType": "glycosylation", "motif": r"N[^P][ST]",
     "riskLevel": "High", "fixability": "fixable"},
    {"id": "deamidation_nahnt", "name": "Deamidation (N[AHNT])",
     "liabilityType": "deamidation", "motif": r"N[AHNT]",
     "riskLevel": "Medium", "fixability": "easily_fixable"},
    {"id": "hydrolysis_np", "name": "Hydrolysis (NP)",
     "liabilityType": "hydrolysis", "motif": r"NP",
     "riskLevel": "Medium", "fixability": "fixable"},
    {"id": "fragmentation_ts", "name": "Fragmentation (TS)",
     "liabilityType": "fragmentation", "motif": r"TS",
     "riskLevel": "Medium", "fixability": "fixable"},
    {"id": "tryptophan_oxidation", "name": "Tryptophan Oxidation (W)",
     "liabilityType": "oxidation", "motif": r"W",
     "riskLevel": "Medium", "fixability": "easily_fixable"},
    {"id": "methionine_oxidation", "name": "Methionine Oxidation (M)",
     "liabilityType": "oxidation", "motif": r"M",
     "riskLevel": "Medium", "fixability": "easily_fixable"},
    {"id": "deamidation_stkn", "name": "Deamidation ([STK]N)",
     "liabilityType": "deamidation", "motif": r"[STK]N",
     "riskLevel": "Low", "fixability": "easily_fixable"},
    {"id": "integrin_binding", "name": "Integrin binding",
     "liabilityType": "integrin", "motif": r"RGD|RYD|KGD|NGR|LDV|DGE|GPR",
     "riskLevel": "Low", "fixability": "easily_fixable"},
    {"id": "contains_stop_codon", "name": "Contains stop codon",
     "liabilityType": "sequence-artifact", "motif": r"\*",
     "riskLevel": "High", "fixability": "disqualifying"},
    {"id": "out_of_frame", "name": "Out of frame",
     "liabilityType": "sequence-artifact", "motif": r"_",
     "riskLevel": "High", "fixability": "disqualifying"},
    {"id": "missing_cysteines", "name": "Missing Cysteines",
     "liabilityType": "cysteine", "motif": None,
     "riskLevel": "High", "fixability": "structural"},
    {"id": "extra_cysteines", "name": "Extra Cysteines",
     "liabilityType": "cysteine", "motif": None,
     "riskLevel": "High", "fixability": "hard_to_fix"},
]

FIXABILITY_WEIGHTS: dict[str, float] = {
    "easily_fixable": 1.0,
    "fixable": 3.0,
    "hard_to_fix": 8.0,
    "structural": 20.0,
    "disqualifying": 0.0,
}
