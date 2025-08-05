""" App Class

Author(s): Lex Albrandt, ***PUT NAME HERE***
Date/version: 08/04/05 v2

Purpose: 
"""
from Ship import Ship
from StarMap import StarMap
from Control_Panel import Control_Panel
from celestial_map import get_initial_planets
from celestial_map import celestial_map
from load_artifacts import get_game_data

class App:
    def __init__(self):
        game_data = get_game_data()     # Fn short, - consider removing this
        initial_planets = get_initial_planets(game_data)
        self.ship = Ship("G.S.S. Old Spice", (0, 0))
        self.star_map = StarMap(game_data["planets"], game_data["target"], game_data["artifacts"])
        self.cel_map = celestial_map(initial_planets)
        self.control_panel = Control_Panel(self.ship)

    def run(self):
        if self.ship and self.star_map:
            # Start the GUI control panel
            self.control_panel.start_gui_loop()
        else:
            # Show error dialog if initialization failed
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Error", "Game not initialized properly!")
                root.destroy()
            except:
                pass