# ============================================================
# CELESTIAL GAZETTEER — Story Point SH-12
#
# User Story (SH-12):
#   "As a Quality Engineer, I want to see a list of celestial
#    artifacts including abandoned freighters, space stations,
#    meteor storms and asteroids so I know where to go in order
#    to interact with a celestial object."
#
# DESIGN DECISIONS:
# - Static data (planets, artifacts) from ARTIFACT.TXT.
# - Dynamic data (discovered artifacts) from celestial_map if provided.

#
# REQUIREMENTS:
# - Show planets and artifacts (freighters, stations, asteroids,
#   wormholes, etc.) with coordinates.
# - Present as a formatted list accessible to the player/tester.
#
# NOT REQUIRED:
# - No restriction to visited only (that's SH-7).
# - No supply/energy/accounting (covered elsewhere).
# - No save/load persistence (that's SH-15).
#
# IMPLEMENTATION NOTES:
# - Uses load_artifacts.get_game_data() to parse ARTIFACT.TXT.
# - Formats planets + artifacts into a CLI-friendly table.
# - Optionally appends "Discovered" entries using celestial_map
#   if provided.
# ============================================================
# source_code/celestial_gazetteer.py

from load_artifacts import get_game_data  # parses ARTIFACT.TXT

def build_gazetteer(cel_map=None, show_discoveries: bool = False) -> str:
    """
    Return a formatted table of celestial artifacts & planets.

    Default (SH-12 pure): static catalog from ARTIFACT.TXT only.
    Optional: if show_discoveries=True and cel_map is provided, append a
              'Discovered' section using cel_map.map_data['visited_info'].
    """
    game = get_game_data()
    planets = game["planets"]       # dict[str, tuple[int,int]]
    artifacts = game["artifacts"]   # dict[str, dict{type, x, y}]

    lines = []
    lines.append("\n=== CELESTIAL GAZETTEER ===")
    lines.append(f"{'Name':<22} {'Type':<20} {'Coordinates':<15}")
    lines.append("-" * 60)

    # Planets (static)
    for name, (x, y) in sorted(planets.items(), key=lambda kv: kv[0].lower()):
        lines.append(f"{name:<22} {'PLANET':<20} ({x},{y})")

    # Artifacts (static)
    for name, data in sorted(artifacts.items(), key=lambda kv: kv[0].lower()):
        lines.append(f"{name:<22} {data['type']:<20} ({data['x']},{data['y']})")

    # Optional: discovered section (from SH-7 data)
    if show_discoveries and cel_map is not None:
        vis_info = getattr(cel_map, "map_data", {}).get("visited_info", {})
        if vis_info:
            lines.append("\n-- Discovered (from visits) --")
            seen = set()
            for pos, info in vis_info.items():
                for art in info.get("artifacts", []):
                    key = (art, pos)
                    if key in seen:
                        continue
                    seen.add(key)
                    # If you don't store type on the map, label as DISCOVERED
                    lines.append(f"{art:<22} {'DISCOVERED':<20} {pos}")

    return "\n".join(lines)
