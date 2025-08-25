"""
Celestial Artifact Placement Test Suite (SH-5)

Author: Hassan Abdi
Date/Version: 08/06/25 v1

Acceptance Criteria (SH-5):
- Artifacts within 2 CP of player location are detected.
- Artifacts exactly 2 CP away are detected.
- Artifacts beyond 2 CP are not detected.
- Collision occurs when player location == artifact CP.
"""


import pytest
from math import dist


@pytest.fixture
def artifacts():
    return {
        "WH-1": {"type": "WORM-HOLE", "x": 37, "y": 35},
        "Flying-Goober": {"type": "BAD-MAX", "x": 105, "y": 105},
        "Asteroid-1": {"type": "ASTEROID", "x": 48, "y": 68}
    }


@pytest.fixture
def player():
    return {"location": (0, 0)}


def detect_artifacts(player_location, artifacts, radius=2):
    detected = []
    for name, data in artifacts.items():
        if dist(player_location, (data["x"], data["y"])) <= radius:
            detected.append(name)
    return detected


def check_collision(player_location, artifacts):
    for name, data in artifacts.items():
        if player_location == (data["x"], data["y"]):
            return name
    return None

def test_artifact_detected_within_1_cp(artifacts):
    player_loc = (48, 67)  # 1 unit away from Asteroid-1
    result = detect_artifacts(player_loc, artifacts)
    assert "Asteroid-1" in result

def test_artifact_detected_exactly_2_cp(artifacts):
    player_loc = (46, 68)  # Exactly 2 units away from Asteroid-1
    result = detect_artifacts(player_loc, artifacts)
    assert "Asteroid-1" in result

def test_artifact_not_detected_beyond_2_cp(artifacts):
    player_loc = (45, 68)  # 3 units away from Asteroid-1
    result = detect_artifacts(player_loc, artifacts)
    assert "Asteroid-1" not in result

def test_artifact_collision(artifacts):
    player_loc = (105, 105)
    collision = check_collision(player_loc, artifacts)
    assert collision == "Flying-Goober"

def test_no_artifact_collision(artifacts):
    player_loc = (105, 104)
    collision = check_collision(player_loc, artifacts)
    assert collision is None

