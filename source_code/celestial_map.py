"""     
Celestial map class

Author: Lex Albrandt
Date/version: 08/20/25 v2
        
Purpose: 
    Contains functions relating to the celestial map
        
Current Methods:
    - visit(position, planet, artifact)
    - print_celestial_map()
    - get_initial_planets(game_data) -> Standalone function
"""

from typing import Dict, Tuple, Any


# Standalone utility functions
def get_initial_planets(game_data: Dict) -> Dict:
    planet_names = ["Celeron", "Xeon", "Ryzen"]
    initial_planets = {}

    for name in planet_names:
        if name in game_data.get("planets", {}):
            initial_planets[name] = game_data["planets"][name]
    return initial_planets


# Classes
class celestial_map:
    
    def __init__(self, initial_planets: Dict) -> None:
        """ Default constructor

            Args:
                initial_planets (Dict): List of initial planets for initialization
                                        of celestial map
            
            Returns: None
        """
        self.map_data = {
            "visited": set(),
            "visited_info": {}
        }

        for name, coords in initial_planets.items():
            coords_tuple = tuple(coords)
            self.map_data["visited"].add(coords_tuple)
            self.map_data["visited_info"][coords_tuple] = {
                "planet": name,
                "artifact": None
            }

    
    def visit(self, position: Tuple, planets: list, artifacts: list) -> None:
        """ Adds a visit to the celestial map with position and any planets or artifacts found

            Args:
                position (Tuple): current position in the form (int, int)
                planets (list): names of planets found
                artifacts (list): names of artifacts found
            Returns: None
        """
        pos_tuple = tuple(position)
        self.map_data["visited"].add(pos_tuple)
        self.map_data["visited_info"][pos_tuple] = {
            "planets": planets,
            "artifacts": artifacts
        }
    
    
    def print_celestial_map(self) -> str:
        """Return a nicely formatted string of the celestial map for GUI display."""
        if not self.map_data["visited_info"]:
            return "No locations visited yet."

        lines = []
        lines.append("\n=== CELESTIAL MAP VISITS ===")
        lines.append(f"{'#':<3} {'Position':<15} {'Planets':<25} {'Artifacts':<25}")
        lines.append("-" * 85)
        for idx, (position, info) in enumerate(self.map_data["visited_info"].items(), 1):
            planets = info.get("planets", [])
            artifacts = info.get("artifacts", [])
            planets_str = ', '.join(planets) if planets else "None"
            artifacts_str = ', '.join(artifacts) if artifacts else "None"
            lines.append(f"{idx:<3} {str(position):<15} {planets_str:<25} {artifacts_str:<25}")
        lines.append("-" * 85)
        return "\n".join(lines)
        
