from load_artifacts import get_game_data
from StarMap import StarMap
from Sensor import Sensor
from Control_Panel import Control_Panel

class Ship:

  # Define max location (applies for both x and y)
  MAX_CP = 128

  def __init__(self, name: str, position: tuple):
    # set ship status
    self.pos = position  # Set the initial position of the ship
    self.energy = 1000
    self.supplies: float = 100    # This is a percentage
    self.money = 1000
    
    # Supply consumption amount - this will represent the supply usage rate
    self.supply_usage_rate = .9      # (supplies * supply_usage_rate) = new_supplies

    self.name = name
    self.sensors: list[Sensor] = []  # Initialize sensors array as empty list
    self.control_panel = Control_Panel(self)

    self.starMap = StarMap(get_game_data()["planets"], get_game_data()["target"], get_game_data()["artifacts"])
    print(f"Ship {self.name} initialized at position {self.pos}")

  def move(self, new_position: tuple):
    # Update the ship's position -- implement here or control panel (your choice) ? SH-1
    self.supplies = round((self.supplies * self.supply_usage_rate), 2)    # update supplies on move
    self.energy = self.energy - 10            # update supplies on move
    self.pos = new_position

    #TODO - Get movemnt to work with sensors to detect celestial objects

    
    return

  def addSensor(self) -> bool:
    """Add a sensor to the ship's sensors array"""

    # Loop through all the sensors and check to see if there is a sensor at current location
    for sensor in self.sensors:
      if sensor.pos == self.pos:
        return False

    new_sensor = Sensor(self.pos)   # Initialize sensor at current position
    self.sensors.append(new_sensor)
    return True

  def start(self):
    """Start the control panel for the ship"""
    if self.control_panel is not None:
      self.control_panel.start_gui_loop()
    else: 
      print("Control panel not initialized.")

