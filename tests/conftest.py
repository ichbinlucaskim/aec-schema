"""Shared fixtures: load valid example JSON files by schema category."""
import json
from pathlib import Path

import pytest

EXAMPLES = Path(__file__).parent.parent / "examples"


def load(schema: str, filename: str) -> dict:
    return json.loads((EXAMPLES / schema / filename).read_text())


@pytest.fixture
def valid_door():
    return load("opening", "valid_door.json")


@pytest.fixture
def valid_exterior_wall():
    return load("wall", "valid_exterior.json")


@pytest.fixture
def valid_panel():
    return load("panel", "valid_exterior_panel.json")


@pytest.fixture
def valid_framing():
    return load("framing", "valid_panel_framing.json")


@pytest.fixture
def valid_bom():
    return load("bom", "valid_bom.json")


@pytest.fixture
def valid_sequence():
    return load("sequence", "valid_member_sequence.json")
