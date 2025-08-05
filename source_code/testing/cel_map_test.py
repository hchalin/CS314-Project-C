""" Celestial Map Class test suite

Author: Lex Albrandt
Date/version: 08/04/25 v1

Purpose:
    Automated testing pytest suite for the celestial map class
"""

# Manually add the source_code directory for the import works
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from celestial_map import celestial_map
from celestial_map import get_initial_planets


@pytest.fixture
def game_data():
    """ Pytest fixture for game data dictionary

    Args: 
        None

    Returns:
        game_data (Dict)
    """
    return {
        "planets" : {
            "Celeron" : (37, 37),
            "Xeon" : (62, 100),
            "Ryzen" : (110, 100)
        }
    }

def test_initialize(game_data):
    """ Test function for proper initialization of the celestial_map 
        class

    Args:
        game_data (_type_): _description_
    
    Returns:
        None
    """
    initial_planets = get_initial_planets(game_data)
    cm = celestial_map(initial_planets)
    
    assert isinstance(cm.map_data["visited"], set) 
    assert isinstance(cm.map_data["visited_info"], dict)
    assert len(cm.map_data["visited"]) == 3
    assert len(cm.map_data["visited_info"]) == 3


def test_visit(game_data):
    """ Test function to ensure visits are logged correctly

    Args:
        game_data (Dict): Python fixture dictionary for game data
    
    Returns:
        None
    """

    initial_planets = get_initial_planets(game_data)
    cm = celestial_map(initial_planets)
    position = (1, 2)
    planet = "Earth"
    artifact = "None"

    cm.visit(position, planet, artifact)

    assert position in cm.map_data["visited"] 
    assert cm.map_data["visited_info"][position]["planet"] == planet
    assert cm.map_data["visited_info"][position]["artifact"] == artifact

    
def test_get_initial_planets(game_data):
    """ Test function to ensure the get_initial_planets function parses
        data and stores it appropriately

    Args:
        game_data (Dict): Python fixture dictionary for game data

    Returns:
        None
    """

    expected = {
        "Celeron" : (37, 37),
        "Xeon" : (62, 100),
        "Ryzen" : (110, 100)
    }
    
    result = get_initial_planets(game_data)
    assert result == expected