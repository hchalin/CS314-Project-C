"""
Sensor Class

Represents a sensor device that can be deployed at specific locations
to monitor and detect objects or activities within a defined search radius.
This class manages sensor positioning and search capabilities for the
G.S.S. Old Spice bridge control system.

Attributes:
    pos (tuple): The (x, y) coordinates of the sensor's position
    search_radius (int): The detection range of the sensor in units

Methods:
    add(): Deploys/activates the sensor at its current position
"""

class Sensor:
  # Attributes

  def __init__(self, pos=(0, 0), search_radius=2):
    self.pos = pos            # Position of the Sensor
    self.search_radius = search_radius 


