# Architecture Decision Records

## ADR-001 — Cross-repo CI: pin the contract by tag, recreate the side-by-side layout (Option A + pinned contract)

**Status:** Accepted

**Context:**
The pipeline is a polyrepo of seven independent GitHub repositories
(`aec-schema`, `wall-extract`, `panel-decompose`, `framing-synth`,
`assembly-sequence`, `aec-ifc-export`, `floorplan-pipeline`), loosely coupled
only by this repo's JSON-Schema contract. Locally they sit side-by-side under a
single `aec-project/` directory and develop against each other with editable
installs (`pip install -e ../aec-schema`, etc.), which `make setup` and every
README assume.

CI was failing for every consumer repo. GitHub Actions checks out a single repo
into `/home/runner/work/<repo>/<repo>/`, so the sibling directories the editable
installs reference (`../aec-schema`, …) do not exist, and `pip install -e
../aec-schema` errors with "No such file or directory". `floorplan-pipeline`
failed worse: a `path: aec-project` checkout combined with
`working-directory: aec-project/floorplan-pipeline` produced the nested
`…/floorplan-pipeline/floorplan-pipeline/aec-project/floorplan-pipeline` path,
because that monorepo-style layout never existed — each repo is its own remote.

Requirements for the fix: each repo's CI must prove it honours a known version
of the contract; local side-by-side editable development must keep working
byte-for-byte; and we did not want to stand up package-publishing infrastructure
for a portfolio.

**Decision:**
Adopt **Option A (multi-repo checkout) with a pinned contract layer.**

- This repo (`aec-schema`) is the stable contract. It is tagged **`v0.1.0`**.
- Every consumer repo's CI does a second `actions/checkout` of
  `ichbinlucaskim/aec-schema` at **`ref: v0.1.0`** into a *sibling* path, plus a
  self-checkout into its own path, recreating the local layout so the existing
  `pip install -e ../aec-schema` works unchanged. So each repo's CI verifies it
  against a **fixed, pinned contract version** — the point of the exercise.
- Component-to-component dependencies (the five non-schema siblings that
  `floorplan-pipeline` integrates) track **`main`** for now, since those repos
  are still moving and none are tagged yet.
- Each repo keeps running **its own test suite in its own CI** (the polyrepo
  norm — independent per-repo verification). `floorplan-pipeline` additionally
  checks out all six siblings and runs the **end-to-end integration** tests.
- Install ordering is preserved: the editable `aec-schema` is installed **before**
  each repo's own `pip install -e ".[dev]"`, because `aec-schema` is not
  published to PyPI and the consumer's declared `aec-schema>=0.1.0` must already
  be satisfied from the editable sibling.
- The fix lives entirely in CI YAML. No `pyproject.toml` dependency lists and no
  source code changed; the local `../X` editable workflow is untouched.

**Why not Option C (publish the contract to an index):**
Publishing `aec-schema` to PyPI (or a private index) and depending on a pinned
version is the industry standard at scale and is the documented **future** step.
It needs a publish pipeline and release discipline that is overkill for a
portfolio. Pinning the contract by git tag gives the same "verify against a
fixed contract version" guarantee without that infrastructure.

**Why not Option B (install siblings from a git URL,
`pip install git+https://…`):**
It hard-codes GitHub URLs into CI and risks divergence between the local
editable workflow (`../X`) and CI, so the two could silently test different
things. Option A keeps CI and local using the identical `../X` editable install.

**Consequences / honest trade-offs:**
- Pinning consumers to `aec-schema@v0.1.0` means a consumer must **bump the pin**
  to adopt a new contract version. This is intentional: it insulates each
  consumer from contract drift and makes contract upgrades a deliberate, visible
  change.
- Because the five component repos track `main`, an unrelated push to one
  component's `main` can turn another repo's (or `floorplan-pipeline`'s) CI red
  until those components stabilise. Accepted for now.
- Each consumer workflow now lists its sibling deps and a ref — a small amount of
  duplicated CI config, the cost of keeping coupling in CI rather than code.

**Known follow-ups:**
- Tag the five component repos once their interfaces stabilise, then pin
  `floorplan-pipeline`'s component checkouts to those tags instead of `main`.
- Migrate to Option C (publish `aec-schema` as a versioned package) if this
  outgrows portfolio scale.
