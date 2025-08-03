from load_artifacts import get_game_data
from StarMap import StarMap
from Sensor import Sensor
from Control_Panel import Control_Panel

class Ship:
  def __init__(self, name: str, position: tuple):
    self.name = name
    self.pos = position  # Set the initial position of the ship
    self.sensors = [Sensor()]  # Initialize sensors array (blank rn)
    self.control_panel = Control_Panel(self)

    self.starMap = StarMap(get_game_data()["planets"], get_game_data()["target"], get_game_data()["artifacts"])
    print(f"Ship {self.name} initialized at position {self.pos}")

  def move(self, new_position: tuple):
    # Update the ship's position -- implement here or control panel (your choice) ? SH-1
    pass

  def addSensor(self):
    """Add a sensor to the ship's sensors array"""
    new_sensor = Sensor(self.pos)   # Initialize sensor at current position
    self.sensors.append(new_sensor)
    print(f"Sensor added at loc: {self.pos}. Total sensors: {len(self.sensors)}")

  def start(self):
    """Start the control panel for the ship"""
    if self.control_panel is not None:
      self.control_panel.start_gui_loop()
    else: 
      print("Control panel not initialized.")
