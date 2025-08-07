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
        super().__init__(self.__message)

class WormholeException(Exception):
    def __init__(self, message):
        self.__message = message
        super().__init__(self.__message)

class Ship:

  def __init__(self, name: str, position: tuple):
    # set ship status
    self.__supplies = shared_items.supplies
    self.__energy = shared_items.energy
    self.__position = [shared_items.current_x, shared_items.current_y]
    self.__supply_useage = shared_items.supply_useage
    self.__engine_type = shared_items.starting_engine
    self.__boundary = shared_items.max
    self.__money = shared_items.starting_cash
    self.__name = name
    self.__sensors: list[Sensor] = []  # Initialize sensors array as empty list
    self.__control_panel = Control_Panel(self)

    self.starMap = StarMap(get_game_data()["planets"], get_game_data()["target"], get_game_data()["artifacts"])
    print(f"Ship {self.__name} initialized at position {self.__position}")

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
  
  def debug_money(self):
     return self.__money
  
  def debug_name(self):
     return self.__name

  def move(self, distance: float, angle: float):
      self.__position[0] += round(distance*math.cos(math.radians(angle)))
      self.__position[1] += round(distance*math.sin(math.radians(angle)))
      self.use_supplies(self.__supply_useage)
      try:
          self.use_energy(self.engine_type(self.__engine_type)*distance)
      except ValueError:
          print(f"The value of {self.__engine_type} is not valid for the engine type")
      self.update_status()
    #TODO - Get movement to work with sensors to detect celestial objects

  def randomize_position(self):
      self.__position = [round(random.random() * self.__boundary * 2 - self.__boundary), round(random.random() * self.__boundary * 2 - self.__boundary)]
        
  def update_status(self):
      if self.__energy <= 0 or self.__supplies <= 0:
          if shared_items.playstyle == "regular play":
              #raise death exception
              raise DeathException("Out of", "energy" if self.__energy <= 0 else "supplies")
              pass
          elif shared_items.playstyle != "never dies":
              raise ValueError
      if self.__position[0] > self.__boundary or self.__position[0] < -self.__boundary or self.__position[1] > self.__boundary or self.__position[1] < -self.__boundary:
          if shared_items.set_wormhole == "no":
              self.randomize_position()
          else:
              self.__position[0] = shared_items.set_position[0]
              self.__position[1] = shared_items.set_position[1]
          #raise wormhole exception
          raise WormholeException("Hit a wormhole due to being out of bounds")

  def addSensor(self) -> bool:
    """Add a sensor to the ship's sensors array"""

    # Loop through all the sensors and check to see if there is a sensor at current location
    for sensor in self.__sensors:
      if sensor.__position == self.__position:
        return False

    new_sensor = Sensor(self.__position)   # Initialize sensor at current position
    self.__sensors.append(new_sensor)
    return True

  def start(self):
    """Start the control panel for the ship"""
    if self.__control_panel is not None:
      self.__control_panel.start_gui_loop()
    else: 
      print("Control panel not initialized.")