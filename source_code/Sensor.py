"""
Sensor Class

Represents a sensor device that can be deployed at specific locations
to monitor and detect objects or activities within a defined search radius.
This class manages sensor positioning and search capabilities for the
G.S.S. Old Spice bridge control system.

Attributes:
    pos (tuple): The (x, y) coordinates of the sensor's position
    search_radius (int): The detection range of the sensor in units
    star_map (StarMap): Reference to the star map containing known celestial objects
    celestial_map (celestial_map): Reference to the celestial map for recording discoveries

Methods:
    __init__(pos, search_radius, star_map, celestial_map): Initialize sensor with position and both maps
    scan(pos): Scan for celestial objects within search radius and update celestial map
"""
import StarMap

class Sensor:

  def __init__(self, pos=(0, 0), search_radius=2, star_map: StarMap = None, celestial_map=None):
    self.pos = pos            # Position of the Sensor
    self.search_radius = search_radius  # This will be 2 CP's in every direction
    self.star_map = star_map
    self.celestial_map = celestial_map

    # After sensor creation, start the scan
    # Then send the data to the celestial map
    ##self.scan(self.pos)

  def scan(self, pos: tuple)->list:
    '''
    Scan for celestial objects within the sensor's search radius.
    Returns a list of detected objects and adds them to the celestial map.

    '''

    print(f'\nStart scan at position {self.pos} with radius {self.search_radius}')

    detected_objects = []
    
    if not self.star_map:
      print('No star map available for scanning')
      return detected_objects

    x, y = self.pos[0], self.pos[1]
    
    # Define scan boundaries, search radius is 2 until upgraded
    x_min = x - self.search_radius
    x_max = x + self.search_radius
    y_min = y - self.search_radius
    y_max = y + self.search_radius
    
    planet_found: bool = False
    artifact_found: bool = False
    
    # Check planets within range
    for planet_name, planet_pos in self.star_map.planets.items():   # use the items method to iterate the dictionary!
      px, py = planet_pos   # define positions
      if x_min <= px <= x_max and y_min <= py <= y_max:
        detected_objects.append({
          'type': 'PLANET',
          'name': planet_name,
          'position': planet_pos
        })
        planet_found = True
        print(f"Detected planet: {planet_name} at {planet_pos}")
    
    # Check artifacts within range
    for artifact_name, artifact_data in self.star_map.artifacts.items():
      ax, ay = artifact_data['x'], artifact_data['y']
      if x_min <= ax <= x_max and y_min <= ay <= y_max:
        detected_objects.append({
          'type': artifact_data['type'],
          'name': artifact_name, 'position': (ax, ay) })
        artifact_found = True
        print(f"Detected {artifact_data['type']}: {artifact_name} at ({ax}, {ay})")
    
    '''
      Check if target is within range
    '''
    if self.star_map.target in self.star_map.planets:
      target_pos = self.star_map.planets[self.star_map.target]
      tx, ty = target_pos
      if x_min <= tx <= x_max and y_min <= ty <= y_max:
        print(f"TARGET DETECTED: {self.star_map.target} at {target_pos}")
    
    '''
     Add detected objects to celestial map
    '''

    if self.celestial_map and (planet_found or artifact_found):
      
      # Add each object found as a separate entry
      for obj in detected_objects:
        if obj['type'] == 'PLANET':
          self.celestial_map.visit(obj['position'], obj['name'], None)
          print(f"{obj['position']}, {obj['name']}, none")
        else:
          self.celestial_map.visit(obj['position'], None, obj['name'])
      print(f"Added scan results to celestial map at position {self.pos}")


    """ Scratching this for now (see commit 08/21)
    if self.celestial_map and (planet_found or artifact_found):
      self.celestial_map.visit(self.pos, planet_found, artifact_found)                              
      print(f"Added scan results to celestial map at position {self.pos}")
    elif self.celestial_map:
      # Even if nothing found, record the visit
      self.celestial_map.visit(self.pos, None, None)
      print(f"Added empty scan to celestial map at position {self.pos}")
    """ 

    print(f"Scan complete. Found {len(detected_objects)} objects.")
    return detected_objects



