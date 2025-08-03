
from Ship import Ship
from StarMap import StarMap
from Control_Panel import Control_Panel
from load_artifacts import get_game_data

class App:
    def __init__(self):
        game_data = get_game_data()     # Fn short, - consider removing this
        self.ship = Ship("G.S.S. Old Spice", (0, 0))
        self.star_map = StarMap(game_data["planets"], game_data["target"], game_data["artifacts"])
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