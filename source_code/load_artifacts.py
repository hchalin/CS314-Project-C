import os
# This code is designed to load artifacts from a text file
def get_game_data(filename="ARTIFACT.TXT"):
    # I added a relative path to the ARTIFACT.TXT file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    
    artifacts = {}
    planets = {}
    target = None
    section = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line == "PLANETS":
                section = "planets"
                continue
            elif line == "TARGET":
                section = "target"
                continue
            elif line == "ARTIFACTS":
                section = "artifacts"
                continue
            if section == "planets":
                name, coords = line.split()
                x, y = map(int, coords.split(','))
                planets[name] = (x, y)
            elif section == "target":
                target = line
            elif section == "artifacts":
                parts = line.split()
                if len(parts) >= 3:
                    name = parts[0]
                    artifact_type = parts[1]
                    x, y = map(int, parts[2].split(','))
                    artifacts[name] = {"type": artifact_type, "x": x, "y": y}

    return {
        "planets": planets,
        "target": target,
        "artifacts": artifacts
    }
