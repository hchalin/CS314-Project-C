
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
  pos: int = {0,0}            # Position of the Sensor
  search_radius: int = 0      # Search radius capability of the Sesor

  def __init__(self):
    pass

  def add(self) -> None:
    print("Add Sensor!")

