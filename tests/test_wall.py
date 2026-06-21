import json
from pathlib import Path

import pytest

from aec_schema import ValidationError, validate_wall

EXAMPLES = Path(__file__).parent.parent / "examples" / "wall"


def _load(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text())


class TestValidWall:
    def test_exterior_wall_passes(self, valid_exterior_wall):
        validate_wall(valid_exterior_wall)

    def test_interior_wall_passes(self):
        validate_wall(_load("valid_interior.json"))

    def test_schema_version_present(self, valid_exterior_wall):
        assert "schema_version" in valid_exterior_wall


class TestInvalidWall:
    def test_bad_type_raises(self):
        with pytest.raises(ValidationError):
            validate_wall(_load("invalid_bad_type.json"))

    def test_missing_id_raises(self, valid_exterior_wall):
        bad = {k: v for k, v in valid_exterior_wall.items() if k != "id"}
        with pytest.raises(ValidationError):
            validate_wall(bad)

    def test_missing_schema_version_raises(self, valid_exterior_wall):
        bad = {k: v for k, v in valid_exterior_wall.items() if k != "schema_version"}
        with pytest.raises(ValidationError):
            validate_wall(bad)

    def test_invalid_point_raises(self, valid_exterior_wall):
        bad = {**valid_exterior_wall, "start": {"x": "not_a_number", "y": 0}}
        with pytest.raises(ValidationError):
            validate_wall(bad)

    def test_zero_thickness_raises(self, valid_exterior_wall):
        bad = {**valid_exterior_wall, "thickness": 0}
        with pytest.raises(ValidationError):
            validate_wall(bad)

    def test_additional_property_raises(self, valid_exterior_wall):
        bad = {**valid_exterior_wall, "fire_resistance": "1hr"}
        with pytest.raises(ValidationError):
            validate_wall(bad)
