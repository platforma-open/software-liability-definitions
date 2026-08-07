# @platforma-open/milaboratories.software-liability-definitions

## 1.1.0

### Minor Changes

- 0b3dd70: Populate the liability taxonomy: all fifteen definitions plus the fixability weights.

  Each entry carries `id`, `name`, `liabilityType`, `motif`, `riskLevel` and `fixability`. `motif` is
  `null` for the two cysteine-state liabilities, which are counted against expected positions rather
  than matched. The scaffold emitted an empty taxonomy and exited non-zero; it now writes the real
  `{schemaVersion, liabilities, fixabilityWeights}` document.

## 1.0.0

Initial scaffold.
