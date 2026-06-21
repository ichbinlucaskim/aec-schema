import json
from pathlib import Path

import pytest

from aec_schema import ValidationError, validate_bom

EXAMPLES = Path(__file__).parent.parent / "examples" / "bom"


def _load(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text())


class TestValidBom:
    def test_bom_passes(self, valid_bom):
        validate_bom(valid_bom)

    def test_schema_version_present(self, valid_bom):
        assert "schema_version" in valid_bom

    def test_bom_without_sheathing_passes(self, valid_bom):
        no_sheathing = {k: v for k, v in valid_bom.items() if k != "sheathing_area_m2"}
        validate_bom(no_sheathing)


class TestInvalidBom:
    def test_missing_panel_id_raises(self):
        with pytest.raises(ValidationError):
            validate_bom(_load("invalid_missing_panel_id.json"))

    def test_missing_schema_version_raises(self, valid_bom):
        bad = {k: v for k, v in valid_bom.items() if k != "schema_version"}
        with pytest.raises(ValidationError):
            validate_bom(bad)

    def test_empty_items_raises(self, valid_bom):
        bad = {**valid_bom, "items": []}
        with pytest.raises(ValidationError):
            validate_bom(bad)

    def test_zero_count_raises(self, valid_bom):
        bad_items = [{**valid_bom["items"][0], "count": 0}]
        bad = {**valid_bom, "items": bad_items}
        with pytest.raises(ValidationError):
            validate_bom(bad)

    def test_bad_section_raises(self, valid_bom):
        bad_items = [{**valid_bom["items"][0], "section": "4x4"}]
        bad = {**valid_bom, "items": bad_items}
        with pytest.raises(ValidationError):
            validate_bom(bad)

    def test_additional_property_raises(self, valid_bom):
        bad = {**valid_bom, "supplier": "BuildCo"}
        with pytest.raises(ValidationError):
            validate_bom(bad)
