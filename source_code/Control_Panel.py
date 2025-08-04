"""
Control_Panel Class

Manages the ship's control panel operations including movement commands,
sensor deployment, and resource monitoring. Provides both GUI and 
command-line interfaces with looping functionality for continuous operation.

This class serves as the main interface between the user and the ship's systems.
"""

import tkinter as tk
from tkinter import messagebox
from Sensor import Sensor
import load_artifacts
from celestial_map import celestial_map
from celestial_map import get_initial_planets

class Control_Panel:
    def __init__(self, ship):
        self.ship = ship
        self.sensor = Sensor()
        self.running = False
        self.gui_root = None
        
        # Load game data
        game_data = load_artifacts.get_game_data()          # This is redundant, but kept for clarity
        self.artifacts = game_data["artifacts"]
        self.planets = game_data["planets"]
        self.target_planet = game_data["target"]

        # Load the celestial map
        initial_planets = get_initial_planets(game_data)
        self.map = celestial_map(initial_planets)

        # GUI elements (will be set when GUI is created)
        self.location_field = None
        self.message_field = None
        self.energy_field = None
        self.supplies_field = None
        self.money_field = None

    
    def start_gui_loop(self):
        """Start the GUI control panel with continuous loop"""
        self.running = True
        self._create_gui()
        if self.gui_root:
            self.gui_root.mainloop()
    
    def stop(self):
        """Stop the control panel loop"""
        self.running = False
        if self.gui_root:
            self.gui_root.quit()
    
    def _handle_movement(self, direction):
        """Handle ship movement in specified direction"""
        # TODO: Implement movement logic 
        if self.message_field:
            self.message_field.config(text=f"Movement {direction} - Not implemented yet")

    def _handle_sensor_deployment(self):
        """Handle sensor deployment at current ship position"""
        self.ship.addSensor()
    
    def _display_status(self):
        """Display current ship status in a popup window"""
        if self.gui_root:
            status_info = (
                f"Ship: {self.ship.name}\n"
                f"Position: {self.ship.pos}\n"
                f"Energy: *energy*\n"
                f"Supplies: *supplies*\n"
                f"Money: *money*\n"
                f"Target Planet: {self.target_planet}\n"
                f"Planets in system: {len(self.planets)}\n"
                f"Artifacts detected: {len(self.artifacts)}"
            )
            messagebox.showinfo("Ship Status", status_info)
            
    def _display_cel_map(self):
        """Display celestial map in a popup window"""
        if self.gui_root:
            info_str = self.map.print_celestial_map()
            messagebox.showinfo("Celestial Map", info_str)
        
    
    def _create_gui(self):
        """Create the GUI control panel"""
        try:
            self.gui_root = tk.Tk()
            self.gui_root.title(f"{self.ship.name} - Control Panel")
            self.gui_root.geometry("600x600")
            
            # Configure grid
            for i in range(9):
                self.gui_root.rowconfigure(i, weight=1)
            for i in range(9):
                self.gui_root.columnconfigure(i, weight=1)
            
            # Ship identifier
            ship_identifier = tk.Label(self.gui_root, 
                                     text=f"{self.ship.name} Bridge Display", 
                                     font=("Arial", 12, "bold"))
            ship_identifier.grid(column=0, row=0, columnspan=3, sticky="SW")
            
            # Directional buttons
            up_button = tk.Button(self.gui_root, text="UP", 
                                command=lambda: self._handle_movement("up"))
            up_button.grid(column=1, row=1, sticky="S")
            
            left_button = tk.Button(self.gui_root, text="LEFT", 
                                  command=lambda: self._handle_movement("left"))
            left_button.grid(column=0, row=2, sticky="E")
            
            right_button = tk.Button(self.gui_root, text="RIGHT", 
                                   command=lambda: self._handle_movement("right"))
            right_button.grid(column=2, row=2, sticky="W")
            
            down_button = tk.Button(self.gui_root, text="DOWN", 
                                  command=lambda: self._handle_movement("down"))
            down_button.grid(column=1, row=3, sticky="N")
            
            # Status button
            status_button = tk.Button(self.gui_root, text="STATUS", 
                                    command=self._display_status)
            status_button.grid(column=3, row=2)
            
            # Sensor button
            sensor_button = tk.Button(self.gui_root, text="Add Sensor", 
                                    command=self._handle_sensor_deployment)
            sensor_button.grid(column=4, row=2)
            
            # Celestial map bbutton
            map_button = tk.Button(self.gui_root, text="Map",
                                    command=self._display_cel_map)
            map_button.grid(column=5, row=2)
            
            # Information display
            tk.Label(self.gui_root, text="Current Location").grid(column=0, row=4)
            self.location_field = tk.Label(self.gui_root, text=str(self.ship.pos))
            self.location_field.grid(column=1, row=4, sticky="W")
            
            tk.Label(self.gui_root, text="Energy").grid(column=0, row=5)
            self.energy_field = tk.Label(self.gui_root, text="1000")
            self.energy_field.grid(column=1, row=5, sticky="W")
            
            tk.Label(self.gui_root, text="Supplies").grid(column=0, row=6)
            self.supplies_field = tk.Label(self.gui_root, text="100%")
            self.supplies_field.grid(column=1, row=6, sticky="W")
            
            tk.Label(self.gui_root, text="Money").grid(column=0, row=7)
            self.money_field = tk.Label(self.gui_root, text="1000")
            self.money_field.grid(column=1, row=7, sticky="W")
            
            tk.Label(self.gui_root, text="Message").grid(column=0, row=8)
            self.message_field = tk.Label(self.gui_root, text="Control panel ready")
            self.message_field.grid(column=1, row=8, sticky="W")
            
            # Quit button
            quit_button = tk.Button(self.gui_root, text="QUIT", 
                                  command=self.stop, bg="red", fg="white")
            quit_button.grid(column=4, row=8)                   # Assign quit button to last row
            
        except Exception as e:
            # If GUI creation fails, create a simple error dialog
            try:
                import tkinter as tk_local
                from tkinter import messagebox as mb_local
                root = tk_local.Tk()
                root.withdraw()  # Hide the root window
                mb_local.showerror("Error", f"Failed to create GUI: {e}")
                root.destroy()
            except:
                pass  # Silently fail if even basic tkinter doesn't work
            self.gui_root = None
    
    def update_display(self):
        """Update the display fields (useful for external updates)"""
        if self.location_field:
            self.location_field.config(text=str(self.ship.pos))
        # Add more field updates as needed
