"""
aec-schema — JSON Schema contract layer for the AEC ML pipeline.

Each validate_* function raises jsonschema.ValidationError on failure
and returns None on success.

Usage
-----
>>> from aec_schema import validate_wall, validate_framing, ValidationError
>>> validate_wall(wall_dict)        # raises if invalid
>>> validate_framing(framing_dict)  # raises if invalid
"""
from __future__ import annotations

from typing import Any

from ._validator import ValidationError, validate, validate_sequence_dag

__all__ = [
    "ValidationError",
    "validate_opening",
    "validate_wall",
    "validate_panel",
    "validate_framing",
    "validate_bom",
    "validate_sequence",
]
__version__ = "0.1.0"


def validate_opening(instance: dict[str, Any]) -> None:
    """Validate an Opening object."""
    validate(instance, "opening.schema.json")


def validate_wall(instance: dict[str, Any]) -> None:
    """Validate a Wall segment object."""
    validate(instance, "wall.schema.json")


def validate_panel(instance: dict[str, Any]) -> None:
    """Validate a Panel object."""
    validate(instance, "panel.schema.json")


def validate_framing(instance: dict[str, Any]) -> None:
    """Validate a Framing assembly object.

    In addition to JSON Schema validation, enforces that member_count equals
    len(members) — cross-field equality that JSON Schema cannot express.
    """
    validate(instance, "framing.schema.json")
    actual = len(instance.get("members", []))
    declared = instance.get("member_count", 0)
    if actual != declared:
        raise ValidationError(
            f"member_count ({declared}) does not match actual member count ({actual})"
        )


def validate_bom(instance: dict[str, Any]) -> None:
    """Validate a Bill of Materials object."""
    validate(instance, "bom.schema.json")


def validate_sequence(instance: dict[str, Any]) -> None:
    """Validate an Assembly Sequence object.

    Performs JSON Schema validation then DAG cycle detection via NetworkX.
    """
    validate(instance, "sequence.schema.json")
    validate_sequence_dag(instance)
