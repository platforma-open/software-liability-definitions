# software-liability-definitions

The canonical antibody chemical-liability taxonomy, published as one
[Platforma](https://platforma.bio) software package. One definitional source for every block that
scans, scores, or repairs liabilities. Definitions only — **never a scan**. SDK docs:
[docs.platforma.bio](https://docs.platforma.bio).

Published as `@platforma-open/milaboratories.software-liability-definitions`, entrypoint `main`.

## How a block consumes it

```go
defsSw := assets.importSoftware("@platforma-open/milaboratories.software-liability-definitions:main")
// ... exec.builder().software(defsSw) ... then read the JSON it writes
```

Runs under `@platforma-open/milaboratories.runenv-python-3:3.12.10`, the base Python runenv. The
emitter is standard library only — `src/requirements.txt` lists nothing.

One extra exec per run buys one definitional source. That is the price of the python one-source-root
rule: a python artifact takes exactly one `root`, and each block is its own git repo, so no shared
source tree exists.

## Consumers

| Block | State |
|---|---|
| `antibody-variant-designer` | new — will read this package from the start; not wired yet |
| `antibody-sequence-liabilities` | to migrate — replace `liabilities-calc-script/src/definitions.py` |
| `3D-Structure-Based-Liabilities` | to migrate — replace the literal in `software/liabilities-script/motifs.py` |

No block imports the package yet. Migrating both shipped blocks is what discharges the parity check
their copies currently owe each other.

## Development

```bash
pnpm install
pnpm run build                      # pl-pkg build
uv run --group dev pytest -q        # pins the emitted shape and the transcribed values
```

The suite needs no backend.

### Local dev

`pnpm run build` writes descriptors that point at this working copy. From the consuming block root,
`pnpm run build:dev` then produces a `.sw.json` with `local.path` into this source — no docker build,
no upload. That works against a **local** backend only.

### Remote dev

A K8s Platforma cannot read a developer's filesystem, so the software must arrive as a docker image.
From the consuming block root:

```bash
pnpm run build:dev-remote
```

It builds a `linux/amd64` image per entrypoint, pushes it to the dev ECR
`public.ecr.aws/u5p1x5q2/pl-containers`, and rewrites the `.sw.json` `docker.tag` fields. K8s nodes
pull anonymously — nothing to configure cluster-side. On a 403 or an expired token:

```bash
aws sso login && aws ecr-public get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin public.ecr.aws
```

## Releasing

1. `pnpm changeset` — every change to the taxonomy needs a version bump. CI does not re-upload an
   existing version, so without a bump the registry keeps serving the old artifact under the same
   version string.
2. Merge to `main`; CI publishes.

Verify the upload:

```bash
curl -sI "https://bin.pl-open.science/software/platforma-open/milaboratories.software-liability-definitions/main/<version>.tgz" | head -2
```

200 = published, 404 = not yet.

## License

MIT — see [LICENSE](LICENSE).
