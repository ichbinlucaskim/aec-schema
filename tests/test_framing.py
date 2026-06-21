import json
from pathlib import Path

import pytest

from aec_schema import ValidationError, validate_framing

EXAMPLES = Path(__file__).parent.parent / "examples" / "framing"


def _load(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text())


class TestValidFraming:
    def test_panel_framing_passes(self, valid_framing):
        validate_framing(valid_framing)

    def test_schema_version_present(self, valid_framing):
        assert "schema_version" in valid_framing

    def test_member_count_matches(self, valid_framing):
        assert valid_framing["member_count"] == len(valid_framing["members"])

    def test_has_bottom_plate(self, valid_framing):
        roles = {m["role"] for m in valid_framing["members"]}
        assert "bottom_plate" in roles

    def test_has_double_top_plate(self, valid_framing):
        top_plates = [m for m in valid_framing["members"] if m["role"] == "top_plate"]
        assert len(top_plates) >= 2


class TestInvalidFraming:
    def test_unknown_member_type_raises(self):
        with pytest.raises(ValidationError):
            validate_framing(_load("invalid_unknown_member_type.json"))

    def test_missing_panel_id_raises(self, valid_framing):
        bad = {k: v for k, v in valid_framing.items() if k != "panel_id"}
        with pytest.raises(ValidationError):
            validate_framing(bad)

    def test_missing_schema_version_raises(self, valid_framing):
        bad = {k: v for k, v in valid_framing.items() if k != "schema_version"}
        with pytest.raises(ValidationError):
            validate_framing(bad)

    def test_member_count_mismatch_raises(self, valid_framing):
        bad = {**valid_framing, "member_count": valid_framing["member_count"] + 1}
        with pytest.raises(ValidationError):
            validate_framing(bad)

    def test_member_count_undercount_raises(self, valid_framing):
        bad = {**valid_framing, "member_count": valid_framing["member_count"] - 1}
        with pytest.raises(ValidationError):
            validate_framing(bad)

    def test_empty_members_raises(self, valid_framing):
        bad = {**valid_framing, "members": [], "member_count": 0}
        with pytest.raises(ValidationError):
            validate_framing(bad)

    def test_bad_section_raises(self, valid_framing):
        bad_members = [
            {**valid_framing["members"][0], "section": "2x3.5"} if i == 0 else m
            for i, m in enumerate(valid_framing["members"])
        ]
        bad = {**valid_framing, "members": bad_members}
        with pytest.raises(ValidationError):
            validate_framing(bad)
