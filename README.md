# aec-schema

> JSON Schema contract layer for a modular AEC ML pipeline.

## Why a separate schema package?

Modern ML pipelines for AEC (Architecture, Engineering, Construction) are built as loosely coupled stages, not monoliths. Each processing stage — wall extraction, panel decomposition, framing synthesis, assembly sequencing, IFC export — is an independent service that reads and writes well-defined JSON documents. This package defines those documents. Every downstream repo imports and validates against it, which means any stage can be replaced, rewritten, or tested in isolation without touching the others.

This mirrors how production ML systems are built: data contracts decouple producers from consumers. Promise Robotics-style panelized construction pipelines, where robotic fabrication requires deterministic, machine-readable framing layouts, are a prime example. A shared schema layer ensures that a wall-extraction model and a framing-synthesis model can be developed by separate teams, tested independently, and composed reliably at runtime.

## Schemas

| Schema | Describes | Key fields |
|---|---|---|
| `opening` | Door or window in a wall | type, position, width, height |
| `wall` | Wall segment | start, end, thickness, load_bearing |
| `panel` | Transport/assembly unit | parent_wall, length, height |
| `framing` | Light wood framing assembly | members (stud/plate/header...) |
| `bom` | Bill of materials | items (section, count, total_length_mm) |
| `sequence` | Fabrication/assembly order | level, steps (order, action, depends_on) |

All schemas use **JSON Schema draft 2020-12** with `additionalProperties: false` for strict contracts.

## Usage

```python
from aec_schema import validate_wall, validate_framing, ValidationError

wall = {
    "schema_version": "0.1.0",
    "id": "wall-001",
    "start": {"x": 0.0, "y": 0.0},
    "end": {"x": 3600.0, "y": 0.0},
    "thickness": 140,
    "type": "exterior",
    "load_bearing": True,
}

try:
    validate_wall(wall)
except ValidationError as e:
    print(e.message)
```

### Python-level validation

Two validations go beyond what JSON Schema can express:

- **`validate_framing()`** — enforces that `member_count` equals `len(members)`
- **`validate_sequence()`** — detects dependency cycles in `depends_on` edges using NetworkX DAG analysis

## Install

```bash
pip install -e .           # from repo root
pip install -e ".[dev]"    # with dev dependencies
```

## Unit conventions

All coordinates and lengths are in **millimetres (mm)**. See [docs/units.md](docs/units.md).

## Schema versioning

All schema objects carry a `schema_version` field (`"0.1.0"` currently).
Breaking changes bump the major version. Downstream repos pin to a major version.

## Running tests

```bash
pytest
ruff check src tests
```

## Repo layout

```
src/aec_schema/
├── __init__.py          # public API: validate_opening, validate_wall, ...
├── _validator.py        # jsonschema + networkx validation logic
├── schemas/             # 6 JSON Schema draft 2020-12 files
└── py.typed             # PEP 561 marker

examples/                # valid + invalid JSON for each schema
tests/                   # pytest test suite (one file per schema)
docs/units.md            # unit convention reference
```
