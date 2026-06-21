import json
from pathlib import Path

import pytest

from aec_schema import ValidationError, validate_panel

EXAMPLES = Path(__file__).parent.parent / "examples" / "panel"


def _load(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text())


class TestValidPanel:
    def test_exterior_panel_passes(self, valid_panel):
        validate_panel(valid_panel)

    def test_schema_version_present(self, valid_panel):
        assert "schema_version" in valid_panel

    def test_shear_panel_passes(self, valid_panel):
        shear = {**valid_panel, "id": "panel-shear-001", "panel_type": "shear"}
        validate_panel(shear)


class TestInvalidPanel:
    def test_negative_length_raises(self):
        with pytest.raises(ValidationError):
            validate_panel(_load("invalid_negative_length.json"))

    def test_excessive_length_raises(self, valid_panel):
        bad = {**valid_panel, "length": 3701.0}
        with pytest.raises(ValidationError):
            validate_panel(bad)

    def test_missing_id_raises(self, valid_panel):
        bad = {k: v for k, v in valid_panel.items() if k != "id"}
        with pytest.raises(ValidationError):
            validate_panel(bad)

    def test_missing_schema_version_raises(self, valid_panel):
        bad = {k: v for k, v in valid_panel.items() if k != "schema_version"}
        with pytest.raises(ValidationError):
            validate_panel(bad)

    def test_bad_panel_type_raises(self, valid_panel):
        bad = {**valid_panel, "panel_type": "garage"}
        with pytest.raises(ValidationError):
            validate_panel(bad)

    def test_additional_property_raises(self, valid_panel):
        bad = {**valid_panel, "weight_kg": 450}
        with pytest.raises(ValidationError):
            validate_panel(bad)
