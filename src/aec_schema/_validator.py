"""Shared JSON Schema validation logic using jsonschema + referencing."""
from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any

import networkx as nx
from jsonschema import ValidationError
from jsonschema import validate as _jsonschema_validate

__all__ = ["validate", "validate_sequence_dag", "ValidationError"]


@cache
def _load_schema(name: str) -> dict[str, Any]:
    schema_dir = Path(__file__).parent / "schemas"
    return json.loads((schema_dir / name).read_text())


def validate(instance: dict[str, Any], schema_name: str) -> None:
    """Validate *instance* against the named schema.

    Raises jsonschema.ValidationError if *instance* does not conform.
    """
    schema = _load_schema(schema_name)
    _jsonschema_validate(instance, schema)


def validate_sequence_dag(instance: dict[str, Any]) -> None:
    """Validate that sequence steps form a DAG (no cycles in depends_on edges).

    Raises jsonschema.ValidationError if a dependency cycle is detected.

    Note: referential integrity (depends_on pointing to non-existent target_ids)
    is not checked here — JSON Schema cannot enforce it, and a dangling edge
    without a cycle will not be flagged. Application-layer validation is required
    if referential integrity must be enforced.
    """
    graph: nx.DiGraph = nx.DiGraph()
    for step in instance.get("steps", []):
        target_id = step["target_id"]
        graph.add_node(target_id)
        for dep in step.get("depends_on", []):
            graph.add_edge(dep, target_id)
    if not nx.is_directed_acyclic_graph(graph):
        raise ValidationError("Assembly sequence contains a dependency cycle")
