# software-liability-definitions

The canonical antibody chemical-liability taxonomy, published as one Platforma
software package. One definitional source for every block that scans, scores,
or repairs liabilities.

Published as `@platforma-open/milaboratories.software-liability-definitions`,
entrypoint `main`.

## What it emits

One JSON file: the fifteen liability definitions and the fixability weights.
Definitions only — **never a scan**. The consuming blocks scan differently on
purpose, so a shared scan function would force three behaviours into one.

```json
{
  "schemaVersion": 1,
  "liabilities": [
    {
      "id": "deamidation_ng",
      "name": "Deamidation (N[GS])",
      "liabilityType": "deamidation",
      "motif": "N[GS]",
      "riskLevel": "High",
      "fixability": "fixable"
    }
  ],
  "fixabilityWeights": { "...": 0.0 }
}
```

One entry is six fields:

| Field | Meaning |
|---|---|
| `id` | stable snake_case key, safe as a dict key or column suffix |
| `name` | the display spelling every shipped block already uses — never reworded |
| `liabilityType` | closed set: `deamidation`, `isomerization`, `fragmentation`, `glycosylation`, `hydrolysis`, `oxidation`, `cysteine`, `integrin`, `sequence-artifact` |
| `motif` | regex over one-letter residues, or `null` |
| `riskLevel` | `Low`, `Medium` or `High` |
| `fixability` | `easily_fixable`, `fixable`, `hard_to_fix`, `structural` or `disqualifying` |

`motif: null` means detection is **not** a motif match. It holds for the two
cysteine-state liabilities (`Missing Cysteines`, `Extra Cysteines`), which are
counted against expected positions. A consumer branches on `motif === null`
rather than on a separate detector field, which cannot then contradict the
motif.

`fixability` decides which liabilities the variant designer will try to repair:
`easily_fixable` and `fixable` generate variants, `hard_to_fix` is annotate-only,
and `structural` and `disqualifying` never generate.

`schemaVersion` is bumped whenever a field is added or a field's meaning
changes, so a consumer can refuse a taxonomy it does not understand. Room is
left for a canonical-substitution table, deferred out of V0.5.

The emitted vocabulary is `liabilities`, not `motifHits` — this package fixes
the terms for every consumer.

## How a block consumes it

```go
defsSw := assets.importSoftware("@platforma-open/milaboratories.software-liability-definitions:main")
// ... exec.builder().software(defsSw) ... then read the JSON it writes
```

One extra exec per run buys one definitional source. That is the price of the
python one-source-root rule: a python artifact takes exactly one `root`, and
each block is its own git repo, so no shared source tree exists.

## Consumers

| Block | State |
|---|---|
| `antibody-variant-designer` | new — reads this package from the start |
| `antibody-sequence-liabilities` | to migrate — replace `liabilities-calc-script/src/definitions.py` |
| `3D-Structure-Based-Liabilities` | to migrate — replace the literal in `software/liabilities-script/motifs.py` |

Migrating both shipped blocks is what discharges the parity check their copies
currently owe each other.

## Status

**The taxonomy is populated** — fifteen definitions in `src/definitions.py`.
`main.py` still exits non-zero rather than writing an empty taxonomy. What
remains is migrating the two shipped blocks off their literal copies.

## Development

```bash
pnpm install
pnpm run build                      # pl-pkg build
uv run --group dev pytest -q        # pins the emitted shape and the transcribed values
```
