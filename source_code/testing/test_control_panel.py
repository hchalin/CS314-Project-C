"""
Enhanced Test Script for Control_Panel Class

This script provides comprehensive testing for the ship control panel,
including movement, sensor deployment, and status display functionality.
"""

import sys
import os
import time
# Add the parent directory to the path so we can import from source_code
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Ship import Ship
from Control_Panel import Control_Panel


def test_ship_initialization():
    """Test ship initialization with various parameters"""
    print("Testing ship initialization...")
    
    # Test normal initialization
    ship1 = Ship("G.S.S. Old Spice", (0, 0))
    assert ship1.name == "G.S.S. Old Spice"
    assert ship1.pos == (0, 0)
    assert ship1.energy == 1000
    assert ship1.supplies == 100
    print("✓ Normal ship initialization passed")
    
    # Test different starting positions
    ship2 = Ship("Test Ship", (50, 75))
    assert ship2.pos == (50, 75)
    print("✓ Custom position initialization passed")
    
    return ship1

def test_movement_logic():
    """Test movement functionality without GUI"""
    print("\nTesting movement logic...")
    
    ship = Ship("Movement Test Ship", (5, 5))
    control_panel = Control_Panel(ship)
    
    # Test basic movement
    original_pos = ship.pos
    control_panel._handle_movement("up")
    assert ship.pos == (5, 6), f"Expected (5, 6), got {ship.pos}"
    print("✓ UP movement passed")
    
    control_panel._handle_movement("right")
    assert ship.pos == (6, 6), f"Expected (6, 6), got {ship.pos}"
    print("✓ RIGHT movement passed")
    
    control_panel._handle_movement("down")
    assert ship.pos == (6, 5), f"Expected (6, 5), got {ship.pos}"
    print("✓ DOWN movement passed")
    
    control_panel._handle_movement("left")
    assert ship.pos == (5, 5), f"Expected (5, 5), got {ship.pos}"
    print("✓ LEFT movement passed")
    
    return ship

def test_boundary_conditions():
    """Test movement at boundaries"""
    print("\nTesting boundary conditions...")
    
    # Test at origin
    ship = Ship("Boundary Test Ship", (0, 0))
    control_panel = Control_Panel(ship)
    
    control_panel._handle_movement("left")
    assert ship.pos[0] >= 0, f"X coordinate went negative: {ship.pos}"
    print("✓ Left boundary protection passed")
    
    control_panel._handle_movement("down")
    assert ship.pos[1] >= 0, f"Y coordinate went negative: {ship.pos}"
    print("✓ Down boundary protection passed")
    
    # Test at maximum
    max_pos = ship.MAX_CP - 1
    ship.pos = (max_pos, max_pos)
    
    control_panel._handle_movement("right")
    assert ship.pos[0] < ship.MAX_CP, f"X coordinate exceeded maximum: {ship.pos}"
    print("✓ Right boundary protection passed")
    
    control_panel._handle_movement("up")
    assert ship.pos[1] < ship.MAX_CP, f"Y coordinate exceeded maximum: {ship.pos}"
    print("✓ Up boundary protection passed")

def test_sensor_functionality():
    """Test sensor deployment"""
    print("\nTesting sensor functionality...")
    
    ship = Ship("Sensor Test Ship", (10, 10))
    control_panel = Control_Panel(ship)
    
    initial_sensor_count = len(ship.sensors)
    result = ship.addSensor()
    assert result == True, "Sensor addition should succeed"
    assert len(ship.sensors) == initial_sensor_count + 1, "Sensor count should increase"
    print("✓ Sensor addition passed")
    
    # Test duplicate sensor at same location
    result = ship.addSensor()
    assert result == False, "Duplicate sensor should be rejected"
    assert len(ship.sensors) == initial_sensor_count + 1, "Sensor count should not increase"
    print("✓ Duplicate sensor prevention passed")

def test_supplies_consumption():
    """Test that supplies decrease with movement"""
    print("\nTesting supplies consumption...")
    
    ship = Ship("Supply Test Ship", (5, 5))
    control_panel = Control_Panel(ship)
    
    initial_supplies = ship.supplies
    control_panel._handle_movement("up")
    
    assert ship.supplies < initial_supplies, f"Supplies should decrease after movement: {initial_supplies} -> {ship.supplies}"
    expected_supplies = round(initial_supplies * ship.supply_usage_rate, 2)
    assert ship.supplies == expected_supplies, f"Expected {expected_supplies}, got {ship.supplies}"
    print("✓ Supply consumption passed")

def run_automated_tests():
    """Run all automated tests"""
    print("=" * 50)
    print("RUNNING AUTOMATED TESTS")
    print("=" * 50)
    
    try:
        test_ship_initialization()
        test_movement_logic()
        test_boundary_conditions()
        test_sensor_functionality()
        test_supplies_consumption()
        
        print("\n" + "=" * 50)
        print("ALL AUTOMATED TESTS PASSED! ✓")
        print("=" * 50)
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

def launch_gui_test():
    """Launch the GUI for manual testing"""
    print("\nLaunching GUI for manual testing...")
    print("Test the following manually:")
    print("1. Movement buttons (UP, DOWN, LEFT, RIGHT)")
    print("2. Status button (shows ship information)")
    print("3. Add Sensor button")
    print("4. Map button (if available)")
    print("5. Position display updates")
    print("6. Supply consumption on movement")
    print("7. Quit button functionality")
    
    try:
        ship = Ship("G.S.S. Old Spice", (0, 0))
        control_panel = Control_Panel(ship)
        control_panel.start_gui_loop()
        
    except KeyboardInterrupt:
        print("\nGUI test interrupted by user")
    except Exception as e:
        print(f"\n❌ GUI Error: {e}")
        # Show error in a dialog if possible
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("GUI Test Error", f"Failed to start control panel: {e}")
            root.destroy()
        except:
            pass

def main():
    """Main test function with user menu"""
    print("Control Panel Test Suite")
    print("=" * 30)
    print("1. Run Automated Tests")
    print("2. Launch GUI Test")
    print("3. Run Both")
    print("4. Exit")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_automated_tests()
            
        elif choice == "2":
            launch_gui_test()
            
        elif choice == "3":
            if run_automated_tests():
                print("\nAutomated tests passed! Launching GUI...")
                time.sleep(2)
                launch_gui_test()
            else:
                print("\nAutomated tests failed. Fix issues before GUI testing.")
                
        elif choice == "4":
            print("Exiting test suite...")
            return
            
        else:
            print("Invalid choice. Please select 1-4.")
            main()  # Recursively call main for retry
            
    except KeyboardInterrupt:
        print("\nTest suite interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()
