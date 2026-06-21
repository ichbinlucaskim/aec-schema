import json
from pathlib import Path

import pytest

from aec_schema import ValidationError, validate_sequence

EXAMPLES = Path(__file__).parent.parent / "examples" / "sequence"


def _load(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text())


class TestValidSequence:
    def test_member_sequence_passes(self, valid_sequence):
        validate_sequence(valid_sequence)

    def test_schema_version_present(self, valid_sequence):
        assert "schema_version" in valid_sequence

    def test_panel_level_passes(self):
        seq = {
            "schema_version": "0.1.0",
            "level": "panel",
            "steps": [
                {"order": 0, "target_id": "panel-001", "action": "erect_panel"},
                {
                    "order": 1,
                    "target_id": "panel-002",
                    "action": "erect_panel",
                    "depends_on": ["panel-001"],
                },
            ],
        }
        validate_sequence(seq)

    def test_dangling_depends_on_passes_schema(self):
        """Known limitation: JSON Schema cannot enforce referential integrity of
        depends_on references. A depends_on pointing to a non-existent target_id
        passes both schema and DAG validation (no cycle is formed). Callers must
        validate referential integrity at the application level if required.
        """
        seq = {
            "schema_version": "0.1.0",
            "level": "member",
            "steps": [
                {
                    "order": 0,
                    "target_id": "step-A",
                    "action": "place_bottom_plate",
                    "depends_on": ["nonexistent-step"],
                }
            ],
        }
        validate_sequence(seq)  # should not raise — known limitation


class TestInvalidSequence:
    def test_dag_cycle_raises(self):
        with pytest.raises(ValidationError):
            validate_sequence(_load("invalid_dependency_cycle.json"))

    def test_missing_schema_version_raises(self, valid_sequence):
        bad = {k: v for k, v in valid_sequence.items() if k != "schema_version"}
        with pytest.raises(ValidationError):
            validate_sequence(bad)

    def test_missing_level_raises(self, valid_sequence):
        bad = {k: v for k, v in valid_sequence.items() if k != "level"}
        with pytest.raises(ValidationError):
            validate_sequence(bad)

    def test_bad_level_enum_raises(self, valid_sequence):
        bad = {**valid_sequence, "level": "assembly"}
        with pytest.raises(ValidationError):
            validate_sequence(bad)

    def test_empty_steps_raises(self, valid_sequence):
        bad = {**valid_sequence, "steps": []}
        with pytest.raises(ValidationError):
            validate_sequence(bad)

    def test_self_loop_raises(self):
        seq = {
            "schema_version": "0.1.0",
            "level": "member",
            "steps": [
                {
                    "order": 0,
                    "target_id": "step-A",
                    "action": "place_bottom_plate",
                    "depends_on": ["step-A"],
                }
            ],
        }
        with pytest.raises(ValidationError):
            validate_sequence(seq)
