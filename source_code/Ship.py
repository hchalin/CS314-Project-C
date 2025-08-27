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

class MovingEntity:
  def __init__(self, use_rand):
    if shared_items.min_energy < 0 or shared_items.min_supplies < 0:
       raise ValueError("Shared_items configuration error: can't have negative minimum vitals")
    if shared_items.max < 1:
       raise ValueError("Shared_items coniguration error: map boundary can't be less than 1")
    if shared_items.min_supplies > shared_items.max_supplies or shared_items.min_energy > shared_items.max_energy:
       raise ValueError("Shared_items coniguration error: mins can't be greater than maxs for vitals")
    
    self._boundary = shared_items.max
    if use_rand:
      # uses average of 2 randoms because middle should be prioritized statistically
      self._supplies = round((random.random() % (shared_items.max_supplies - shared_items.min_supplies + 1) 
                               + random.random() % (shared_items.max_supplies - shared_items.min_supplies + 1)) 
                               / 2 + shared_items.min_supplies)
      self._energy = round((random.random() % (shared_items.max_energy - shared_items.min_energy + 1) 
                      + random.random() % (shared_items.max_energy - shared_items.min_energy + 1)) 
                      / 2 + shared_items.min_energy)
      self.randomize_position()
    else:
      self._supplies = shared_items.supplies
      self._energy = shared_items.energy
      self._position = [shared_items.current_x, shared_items.current_y]

  def debug_position(self):
    return self._position
  
  def use_supplies(self, amount: float):
    self._supplies -= amount

  def use_energy(self, amount: float):
    self._energy -= amount

  def gain_supplies(self, amount: float):
    self._supplies += amount

  def gain_energy(self, amount: float):
    self._energy += amount

  def debug_energy(self):
    return self._energy

  def debug_supplies(self):
    return self._supplies

  def change_position(self, distance, angle):
    self._position[0] += round(distance*math.cos(math.radians(angle)))
    self._position[1] += round(distance*math.sin(math.radians(angle)))

  def randomize_position(self):
      self._position = [round(random.random() * self._boundary * 2 - self._boundary), round(random.random() * self._boundary * 2 - self._boundary)]

  def check_position(self):
      if self._position[0] > self._boundary or self._position[0] < -self._boundary or self._position[1] > self._boundary or self._position[1] < -self._boundary:
          if shared_items.set_wormhole == "no":
              self.randomize_position()
          else:
              self._position[0] = shared_items.set_position[0]
              self._position[1] = shared_items.set_position[1]
          #raise wormhole exception
          raise WormholeException("Hit a wormhole due to being out of bounds")
        
class AbandonFrieghtor(MovingEntity):
  def __init__(self):
     super().__init__(True)
     self._velocity = []

  def apply_velocity(self):
    self.change_position(self._velocity[0], self._velocity[1])
    try:
      self.check_position()
    except WormholeException:
      pass

  def transfer_items(self, looting_ship):
    gained_str = f"Gained {self.debug_energy()} energy and {self.debug_supplies()} supplies from the abandoned freighter.\n"
    looting_ship.gain_energy(self.debug_energy())
    self.use_energy(self.debug_energy())
    looting_ship.gain_energy(self.debug_energy())
    self.use_energy(self.debug_energy())
    return gained_str

class Ship(MovingEntity):
  def __init__(self, name: str, position: tuple):
    # set ship status
    super().__init__(False)
    self._supply_useage = shared_items.supply_useage
    self._engine_type = shared_items.starting_engine
    self._money = shared_items.starting_cash
    self._name = name
    self._sensors: list[Sensor] = []  # Initialize sensors array as empty list
    self._control_panel = Control_Panel(self)

    # Initialize star map
    game_data = get_game_data()
    self.star_map = StarMap(game_data["planets"], game_data["target"], game_data["artifacts"])
    
    print(f"Ship {self._name} initialized at position {self.debug_position()}")

  """
  def move(self, new_position: tuple):
    # Update the ship's position -- implement here or control panel (your choice) ? SH-1
    self.supplies = round((self.supplies * self.supply_usage_rate), 2)    # update supplies on move
    self.energy = self.energy - 10            # update supplies on move
    self.pos = new_position
  """

  def debug_money(self):
     return self._money
  
  def debug_name(self):
     return self._name

  def check_vitals(self):
      if self.debug_energy() <= 0 or self.debug_supplies() <= 0:
          if shared_items.playstyle == "regular play":
              #raise death exception
              raise DeathException(f"Out of {"energy" if self.debug_energy() <= 0 else "supplies"}")
              pass
          elif shared_items.playstyle != "never dies":
              raise ValueError

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
      self.use_supplies(self._supply_useage)
      try:
          self.use_energy(self.engine_type(self._engine_type)*distance)
      except ValueError:
          print(f"The value of {self._engine_type} is not valid for the engine type")
      self.change_position(distance, angle)
      self.check_vitals()
      self.check_position()
    #TODO - Get movement to work with sensors to detect celestial objects

  def addSensor(self, celestial_map) -> bool:
    """Add a sensor to the ship's sensors array and consume 2% supplies"""

    # Loop through all the sensors and check to see if there is a sensor at current location
    for sensor in self._sensors:
      if hasattr(sensor, '_Sensor__position') and sensor._Sensor__position == self._position:
        return None  # Sensor already exists

    # Consume 2% of supplies for sensor deployment
    self.use_supplies(shared_items.sensor_cost)  # 98% remaining (2% consumed)
    
    new_sensor = Sensor(self._position, 2, self.star_map, celestial_map)   # Initialize sensor at current position
    new_sensor.scan(self._position)
    self._sensors.append(new_sensor)                                                   # Added double underscore for fix
    return True

  def start(self):
    """Start the control panel for the ship"""
    if self._control_panel is not None:
      self._control_panel.start_gui_loop()
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