from load_artifacts import get_game_data
from StarMap import StarMap
from Sensor import Sensor
from Control_Panel import Control_Panel
import shared_items
import math
import random

class DeathException(Exception):
    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

class WormholeException(Exception):
    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

class Ship:

  # Define max location (applies for both x and y)
  MAX_CP = 128

  def __init__(self, name: str, position: tuple):
    # set ship status
    self.__supplies = shared_items.supplies
    self.__energy = shared_items.energy
    self.__position = [shared_items.current_x, shared_items.current_y]
    self.__supply_useage = shared_items.supply_useage
    self.__engine_type = shared_items.starting_engine
    self.__boundary = shared_items.max
    
    self.name = name
    self.sensors: list[Sensor] = []  # Initialize sensors array as empty list
    self.control_panel = Control_Panel(self)

    self.starMap = StarMap(get_game_data()["planets"], get_game_data()["target"], get_game_data()["artifacts"])
    print(f"Ship {self.name} initialized at position {self.pos}")

  def use_supplies(self, amount: float):
      self.__supplies -= amount

  def use_energy(self, amount: float):
      self.__energy -= amount

  def debug_energy(self):
      return self.__energy

  def debug_supplies(self):
      return self.__supplies

  def debug_position(self):
      return self.__position

  def move(self, distance: float, angle: float):
      self.__position[0] += distance*math.cos(math.radians(angle))
      self.__position[1] += distance*math.sin(math.radians(angle))
      self.use_supplies(self.__supply_useage)
      try:
          self.use_energy(self.engine_type(self.__engine_type)*distance)
      except ValueError:
          print(f"The value of {self.__engine_type} is not valid for the engine type")
      self.update_status()
    #TODO - Get movemnt to work with sensors to detect celestial objects

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