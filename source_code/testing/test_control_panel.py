"""
FIX: not working, need to fix imports???
"""

from Ship import Ship
from Control_Panel import Control_Panel

def main():
    # Create a ship
    ship = Ship("G.S.S. Old Spice", (0, 0))
    
    # Create control panel
    control_panel = Control_Panel(ship)
    
    print("Select interface:")
    print("1. GUI Control Panel")
    print("2. Command Line Interface")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()       # strip to remove any leading/trailing whitespace
        
        if choice == "1":
            print("Starting GUI control panel...")
            control_panel.start_gui_loop()
        elif choice == "2":
            print("Starting command-line interface...")
            control_panel.start_command_loop()
        else:
            print("Invalid choice. Starting command-line interface...")
            control_panel.start_command_loop()
            
    except KeyboardInterrupt:
        print("\nShutting down control panel...")
    except Exception as e:
        print(f"Error: {e}")
        print("Falling back to command-line interface...")
        control_panel.start_command_loop()

if __name__ == "__main__":
    main()
