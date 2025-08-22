from load_artifacts import get_game_data
from StarMap import StarMap
from Sensor import Sensor
from Control_Panel import Control_Panel
from celestial_map import celestial_map, get_initial_planets
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

    # Initialize star map
    game_data = get_game_data()
    self.star_map = StarMap(game_data["planets"], game_data["target"], game_data["artifacts"])
    
    print(f"Ship {self.__name} initialized at position {self.__position}")

  def move(self, new_position: tuple):
    # Update the ship's position -- implement here or control panel (your choice) ? SH-1
    self.supplies = round((self.supplies * self.supply_usage_rate), 2)    # update supplies on move
    self.energy = self.energy - 10            # update supplies on move
    self.pos = new_position

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

  def engine_type(self, type: str) -> float:
      if type == "basic":
            return 10
          # verify names and stats later
      elif type == "upgraded":
            return 5
      elif type == "pro":
            return 1
      else:
            raise ValueError

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
              raise DeathException(f"Out of {"energy" if self.__energy <= 0 else "supplies"}")
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

  def addSensor(self, celestial_map) -> bool:
    """Add a sensor to the ship's sensors array and consume 2% supplies"""

    # Loop through all the sensors and check to see if there is a sensor at current location
    for sensor in self.__sensors:
      if hasattr(sensor, '_Sensor__position') and sensor._Sensor__position == self.__position:
        return None  # Sensor already exists

    # Consume 2% of supplies for sensor deployment
    self.use_supplies(shared_items.sensor_cost)  # 98% remaining (2% consumed)
    
    new_sensor = Sensor(self.__position, 2, self.star_map, celestial_map)   # Initialize sensor at current position
    new_sensor.scan(self.__position)
    self.__sensors.append(new_sensor)                                                   # Added double underscore for fix
    return True

  def start(self):
    """Start the control panel for the ship"""
    if self.__control_panel is not None:
      self.__control_panel.start_gui_loop()
    else: 
      print("Control panel not initialized.")
      
  def display_celestial_map(self):
    """Display the current celestial map
        NOTE: Keep the print logs for debugging / testing 
    """
    if self.celestial_map:
      print("\n=== CELESTIAL MAP ===")
      print(self.celestial_map.print_celestial_map())   # Call the celestial_map print method
      print("====================\n")
    else:
      print("No celestial map available.")

