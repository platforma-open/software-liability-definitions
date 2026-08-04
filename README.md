# software-liability-definitions

The canonical antibody chemical-liability taxonomy, published as one Platforma
software package. One definitional source for every block that scans, scores,
or repairs liabilities.

Published as `@platforma-open/milaboratories.software-liability-definitions`,
entrypoint `main`.

## What it emits

One JSON file: the liability definitions (motif regex, risk level, fixability)
and the fixability weights. Definitions only — **never a scan**. The consuming
blocks scan differently on purpose, so a shared scan function would force three
behaviours into one.

```json
{
  "schemaVersion": 1,
  "liabilities": [{ "id": "...", "name": "...", "motif": "...", "riskLevel": "...", "fixability": "..." }],
  "fixabilityWeights": { "...": 0.0 }
}
```

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

**The taxonomy is not populated.** `src/definitions.py` holds empty
collections, and `main.py` exits non-zero rather than writing an empty
taxonomy. Fill it from the two copies listed above, then migrate them onto it.

## Development

```bash
pnpm install
pnpm run build      # pl-pkg build
```
