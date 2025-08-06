import shared_items
import numpy
import math
import random

class ship:
    def __init__(self):
        self.__supplies = shared_items.supplies
        self.__energy = shared_items.energy
        self.__position = [shared_items.current_x, shared_items.current_y]
        self.__supply_useage = shared_items.supply_useage
        self.__engine_type = shared_items.starting_engine
        self.__boundary = shared_items.max
    def move(self, distance: float, angle: float):
        self.__position[0] += distance*math.cos(math.radians(angle))
        self.__position[1] += distance*math.sin(math.radians(angle))
        self.use_supplies(self.__supply_useage)
        try:
            self.use_energy(self.engine_type(self.__engine_type)*distance)
        except ValueError:
            print(f"The value of {self.__engine_type} is not valid for the engine type")
        self.update_status()
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
    def randomize_position(self):
        self.__position = [random.random() * self.__boundary * 2 - self.__boundary, random.random() * self.__boundary * 2 - self.__boundary]
    def update_status(self):
        if self.__energy <= 0 or self.__supplies <= 0:
            if shared_items.playstyle == "regular play":
                #raise death exception
                raise ValueError
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