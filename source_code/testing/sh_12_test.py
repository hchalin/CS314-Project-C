# testing/sh_12_test.py
"""
SH-12 — Celestial Gazetteer tests (no imports of Ship or Control_Panel)

- Monkeypatches load_artifacts.get_game_data() for predictable data.
- Verifies build_gazetteer() lists planets and artifacts (static).
- Verifies "Discovered" section when cel_map with visited_info is provided.
"""

import os
import sys
import pytest

# Ensure source_code is importable
HERE = os.path.dirname(__file__)
SRC = os.path.abspath(os.path.join(HERE, ".."))
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from celestial_gazetteer import build_gazetteer


@pytest.fixture
def fake_game_data():
    """Deterministic data for gazetteer tests."""
    return {
        "planets": {
            "Celeron": (35, 37),
            "Xeon": (62, 100),
            "Ryzen": (110, 100),
        },
        "target": "Pentium-5",
        "artifacts": {
            "The_Dutchman": {"type": "ABANDONED-FREIGHTER", "x": 80, "y": 100},
            "WH-1": {"type": "WORM-HOLE", "x": 37, "y": 35},
            "Asteroid-1": {"type": "ASTEROID", "x": 48, "y": 68},
        },
    }


@pytest.fixture(autouse=True)
def patch_get_game_data(monkeypatch, fake_game_data):
    """Make load_artifacts.get_game_data() return our fake dataset."""
    import load_artifacts
    monkeypatch.setattr(load_artifacts, "get_game_data", lambda: fake_game_data)


def test_gazetteer_static_lists_planets_and_artifacts(fake_game_data):
    """Static gazetteer should include all planets and artifacts from ARTIFACT.TXT."""
    text = build_gazetteer(cel_map=None, show_discoveries=False)

    # Header sanity
    assert "CELESTIAL GAZETTEER" in text
    assert "Name" in text and "Type" in text and "Coordinates" in text

    # Planets present with coords and type
    for name, (x, y) in fake_game_data["planets"].items():
        assert name in text
        assert "PLANET" in text
        assert f"({x},{y})" in text

    # Artifacts present with coords and type
    for name, meta in fake_game_data["artifacts"].items():
        assert name in text
        assert meta["type"] in text
        assert f"({meta['x']},{meta['y']})" in text

    # No discovered section in static mode
    assert "Discovered (from visits)" not in text


def test_gazetteer_with_discovered_section():
    """When a cel_map with visited_info is supplied and show_discoveries=True, append 'Discovered'."""
    class DummyCelMap:
        def __init__(self):
            self.map_data = {
                "visited_info": {
                    (42, 43): {"planets": [], "artifacts": ["Ghost-Hub"]},
                    (10, 11): {"planets": [], "artifacts": ["Old-Spire"]},
                }
            }

    cel_map = DummyCelMap()
    text = build_gazetteer(cel_map=cel_map, show_discoveries=True)

    assert "Discovered (from visits)" in text
    # Each discovered artifact should appear with its position
    assert "Ghost-Hub" in text and "(42, 43)" in text
    assert "Old-Spire" in text and "(10, 11)" in text
