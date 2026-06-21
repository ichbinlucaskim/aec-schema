import json
from pathlib import Path

import pytest

from aec_schema import ValidationError, validate_opening

EXAMPLES = Path(__file__).parent.parent / "examples" / "opening"


def _load(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text())


class TestValidOpening:
    def test_door_passes(self, valid_door):
        validate_opening(valid_door)

    def test_window_passes(self):
        validate_opening(_load("valid_window.json"))

    def test_schema_version_present(self, valid_door):
        assert "schema_version" in valid_door


class TestInvalidOpening:
    def test_missing_type_raises(self):
        with pytest.raises(ValidationError):
            validate_opening(_load("invalid_missing_type.json"))

    def test_missing_id_raises(self, valid_door):
        bad = {k: v for k, v in valid_door.items() if k != "id"}
        with pytest.raises(ValidationError):
            validate_opening(bad)

    def test_missing_schema_version_raises(self, valid_door):
        bad = {k: v for k, v in valid_door.items() if k != "schema_version"}
        with pytest.raises(ValidationError):
            validate_opening(bad)

    def test_bad_type_enum_raises(self, valid_door):
        bad = {**valid_door, "type": "skylight"}
        with pytest.raises(ValidationError):
            validate_opening(bad)

    def test_negative_width_raises(self, valid_door):
        bad = {**valid_door, "width": -1.0}
        with pytest.raises(ValidationError):
            validate_opening(bad)

    def test_additional_property_raises(self, valid_door):
        bad = {**valid_door, "fire_rating": "60min"}
        with pytest.raises(ValidationError):
            validate_opening(bad)
