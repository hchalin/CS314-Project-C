"""
THIS IS OLD THAT IS NOW DEPRECATED
REFER TO source_code/Control_Panel.py FOR THE NEW GUI
This file was used to create a simple GUI for the ship control panel.
It includes buttons for movement and sensor deployment, and displays the ship's status.

To run program, execute main.py

"""
import tkinter
from tkinter import messagebox

#imports
import shared_items
import load_artifacts

<<<<<<< HEAD
energy = shared_items.energy
supplies = shared_items.supplies

def check_energy():
    global energy
    energy -= 10
    energy_field.config(text=f"{energy}")
    if (energy < 1):
        messagebox.showinfo("Alert!", "Your energy has fallen below 1.")
        message_field.config(text="The game has ended!")
    return

def check_supplies():
    global supplies
    supplies -= 2
    supplies_field.config(text=f"{supplies}")
    if (supplies < 1):
        messagebox.showinfo("Alert!", "Your supplies has fallen below 1.")
        message_field.config(text="The game has ended!")
    return
=======
# Initialize game data from ARTIFACT.TXT
game_data = load_artifacts.get_game_data()
artifacts = game_data["artifacts"]
planets = game_data["planets"]
target_planet = game_data["target"]
from Sensor import Sensor


# Instantiate sensor
sensor = Sensor()
>>>>>>> 2971cbfce7a2f83a464a90578364a7aa4f78add0

def direction_click(direction):
   global energy
   global supplies
   messagebox.showinfo("Info!","You Pushed "+direction)       #pop up alert box
   location_field.config(text=direction)                      #change text in current location display
   message_field.config(text="Someone's pushing my buttons!") #change the message display
   # this would be a good place to call functions that process the move
   
   check_energy()
   check_supplies()
   return

def sensor_click(loc: tuple)-> None:
   # This function is called when you place a sensor
   sensor.add()
   messagebox.showinfo("Sensor Added", "You have added a sensor at location *loc*\n Search radius: *SR*")
   return


# create pop-up window for supplemental information if needed
#pop_up = tkinter.Tk()
#pop_up.title("Supplemental Information")

# establish the bridge control panel tkinter window
control_panel = tkinter.Tk()
control_panel.title("G.S.S. Old Spice")
control_panel.geometry("600x600")

# establish the control_panel grid
control_panel.rowconfigure(0,weight=3) # ship identifier
control_panel.rowconfigure(1,weight=1) # up
control_panel.rowconfigure(2,weight=1) # left/right
control_panel.rowconfigure(3,weight=1) # down
control_panel.rowconfigure(4,weight=1) # current location
control_panel.rowconfigure(5,weight=1) # energy
control_panel.rowconfigure(6,weight=1) # supplies
control_panel.rowconfigure(7,weight=1) # money
control_panel.rowconfigure(8,weight=3) # message

control_panel.columnconfigure(0,weight=1)
control_panel.columnconfigure(1,weight=3)
control_panel.columnconfigure(2,weight=3)
control_panel.columnconfigure(3,weight=3)
control_panel.columnconfigure(4,weight=3)
control_panel.columnconfigure(5,weight=3)
control_panel.columnconfigure(6,weight=3)
control_panel.columnconfigure(7,weight=3)
control_panel.columnconfigure(8,weight=3)


# display Ship Identifier
ship_identifier = tkinter.Label(control_panel,text="G.S.S. Old Spice Bridge Display", font=("Arial",12,"bold"))
ship_identifier.grid(column=0,row=0,sticky="SW")

# arrange directional buttons
up_button = tkinter.Button(control_panel, text="UP", command = lambda:direction_click("UP"))
up_button.grid(column=1,row=1,sticky="S")
left_button = tkinter.Button(control_panel, text="LEFT", command = lambda:direction_click("LEFT"))
left_button.grid(column=0,row=2,sticky="E")
right_button = tkinter.Button(control_panel, text="RIGHT", command = lambda:direction_click("RIGHT"))
right_button.grid(column=2,row=2,sticky="W")
down_button = tkinter.Button(control_panel, text="DOWN", command = lambda:direction_click("DOWN"))
down_button.grid(column=1,row=3,sticky="N")

# Add sensor to current location button
add_sensor_button = tkinter.Button(control_panel, text="Add Sensor", command= lambda:sensor_click(location_field))
add_sensor_button.grid(column=4, row=2)         # Add Sensor to current location (feel free to move location of the control grid!)

# arrange information display
location_label = tkinter.Label(control_panel,text="Current Location")
location_label.grid(column=0,row=4)
location_field = tkinter.Label(control_panel,text="(0,0)")
location_field.grid(column=1,row=4,sticky="W")
energy_label = tkinter.Label(control_panel,text="Energy")
energy_label.grid(column=0,row=5)
energy_field = tkinter.Label(control_panel,text=f"{energy}")
energy_field.grid(column=1,row=5,sticky="W")
supplies_label = tkinter.Label(control_panel,text="Supplies")
supplies_label.grid(column=0,row=6)
supplies_field = tkinter.Label(control_panel,text=f"{supplies}%")
supplies_field.grid(column=1,row=6,sticky="W")
money_label = tkinter.Label(control_panel,text="Money")
money_label.grid(column=0,row=7)
money_field = tkinter.Label(control_panel,text="1000")
money_field.grid(column=1,row=7,sticky="W")
message_label = tkinter.Label(control_panel,text="Message")
message_label.grid(column=0,row=8)
message_field = tkinter.Label(control_panel,text="No current message")
message_field.grid(column=1,row=8,sticky="W")


control_panel.mainloop()
