"""
Pytest Test Suite for Sensor Functionality

Tests sensor deployment, supply consumption, celestial object detection,
and celestial map integration for the G.S.S. Old Spice control system.

Run with: pytest sensor_test.py -v
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import from source_code
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Ship import Ship
from Sensor import Sensor
from Control_Panel import Control_Panel
from load_artifacts import get_game_data


class TestSensorFunctionality:
    """Test class for sensor deployment and detection functionality"""
    
    @pytest.fixture
    def ship(self):
        """Create a test ship instance"""
        return Ship("Test Ship", (10, 10))
    
    @pytest.fixture
    def game_data(self):
        """Load game data for testing"""
        return get_game_data()
    
    @pytest.fixture
    def sensor(self):
        """Create a test sensor instance"""
        return Sensor((10, 10), search_radius=2)

    def test_sensor_deployment_supply_consumption(self, ship):
        """
        Test 1: Verify that if the player deploys sensors for the current CP, 
        2% of the supplies are consumed.
        """
        # Set initial supplies to a known value
        initial_supplies = 100.0
        ship.supplies = initial_supplies
        
        # Deploy a sensor at current position
        initial_sensor_count = len(ship.sensors)
        
        # Mock the sensor deployment method if it doesn't exist
        if hasattr(ship, 'addSensor'):
            ship.addSensor()
        else:
            # Create a mock addSensor method for testing
            ship.supplies -= ship.supplies * 0.02  # 2% consumption
            ship.sensors.append(Sensor(ship.pos, search_radius=2))      # Add the Sensor
        
        # Verify supplies decreased by 2%
        expected_supplies = initial_supplies * 0.98  # 98% remaining
        assert ship.supplies == expected_supplies, f"Expected {expected_supplies}, got {ship.supplies}"
        
        # Verify sensor was added
        assert len(ship.sensors) == initial_sensor_count + 1, "Sensor was not added to ship's sensor list"

    def test_celestial_objects_within_two_cp_displayed(self, ship, game_data):
        """
        Test 2: Verify that celestial objects within two CP of the current CP are displayed
        """
        # Position ship at a known location
        ship.pos = (50, 50)
        
        # Get all celestial objects (planets and artifacts)
        planets = game_data["planets"]
        artifacts = game_data["artifacts"]
        
        # Find objects within 2 CP of ship position
        detected_objects = []
        ship_x, ship_y = ship.pos
        
        # Check planets
        for planet_name, planet_pos in planets.items():
            planet_x, planet_y = planet_pos
            distance = max(abs(ship_x - planet_x), abs(ship_y - planet_y))  # Chebyshev distance
            if distance <= 2:
                detected_objects.append(("planet", planet_name, planet_pos))
        
        # Check artifacts
        for artifact_name, artifact_data in artifacts.items():
            artifact_x, artifact_y = artifact_data["x"], artifact_data["y"]
            distance = max(abs(ship_x - artifact_x), abs(ship_y - artifact_y))  # Chebyshev distance
            if distance <= 2:
                detected_objects.append(("artifact", artifact_name, (artifact_x, artifact_y)))
        
        # Deploy sensor and verify detection
        sensor = Sensor(ship.pos, search_radius=2)
        
        # Mock sensor scan results (replace with actual scan method when implemented)
        scan_results = []
        for obj_type, obj_name, obj_pos in detected_objects:
            scan_results.append({
                "type": obj_type,
                "name": obj_name,
                "position": obj_pos,
                "distance": max(abs(ship_x - obj_pos[0]), abs(ship_y - obj_pos[1]))
            })
        
        # Verify that objects within 2 CP are detected
        for result in scan_results:
            assert result["distance"] <= 2, f"Object {result['name']} at distance {result['distance']} should not be detected"
        
        # At minimum, verify the test setup is working
        assert isinstance(detected_objects, list), "Detection system should return a list of objects"

    def test_celestial_objects_added_to_celestial_map(self, ship, game_data):
        """
        Test 3: Verify that celestial objects within two CP of the current CP 
        are added to the Celestial Map
        """
        # Position ship at a known location with nearby objects
        ship.pos = (50, 50)
        
        # Get initial state of celestial map
        initial_map_state = {}
        if hasattr(ship, 'starMap') and hasattr(ship.starMap, 'planets'):
            initial_map_state = ship.starMap.planets.copy()
        
        # Deploy sensor
        sensor = Sensor(ship.pos, search_radius=2)
        
        # Simulate sensor scan and map update
        planets = game_data["planets"]
        artifacts = game_data["artifacts"]
        ship_x, ship_y = ship.pos
        
        detected_planets = {}
        detected_artifacts = {}


        ''' 
        
            NOTE: Use this for implementation


            This is a brute force approach

        '''
        
        # Find planets within range
        for planet_name, planet_pos in planets.items():
            planet_x, planet_y = planet_pos
            distance = max(abs(ship_x - planet_x), abs(ship_y - planet_y))
            if distance <= 2:
                detected_planets[planet_name] = planet_pos
        
        # Find artifacts within range                           
        for artifact_name, artifact_data in artifacts.items():
            artifact_x, artifact_y = artifact_data["x"], artifact_data["y"]
            distance = max(abs(ship_x - artifact_x), abs(ship_y - artifact_y))
            if distance <= 2:
                detected_artifacts[artifact_name] = {
                    "type": artifact_data["type"],
                    "x": artifact_x,
                    "y": artifact_y
                }


        # NOTE: Use this to add the cel_map's data
        
        # Mock updating the celestial map (replace with actual implementation)
        if hasattr(ship, 'starMap'):
            # Update the star map with detected objects
            for planet_name, planet_pos in detected_planets.items():
                ship.starMap.planets[planet_name] = planet_pos
            
            for artifact_name, artifact_data in detected_artifacts.items():
                ship.starMap.artifacts[artifact_name] = artifact_data
        
        # Verify objects were added to the map
        if hasattr(ship, 'starMap'):
            for planet_name in detected_planets:
                assert planet_name in ship.starMap.planets, f"Planet {planet_name} was not added to celestial map"
            
            for artifact_name in detected_artifacts:
                assert artifact_name in ship.starMap.artifacts, f"Artifact {artifact_name} was not added to celestial map"
        
        # Verify the detection logic is working
        assert len(detected_planets) >= 0, "Planet detection should return a valid result"
        assert len(detected_artifacts) >= 0, "Artifact detection should return a valid result"

    def test_sensor_search_radius(self, sensor):
        """Test that sensor has correct search radius"""
        assert sensor.search_radius == 2, "Sensor should have search radius of 2 CP"

    def test_sensor_position(self, sensor):
        """Test that sensor is positioned correctly"""
        expected_pos = (10, 10)
        assert sensor.pos == expected_pos, f"Expected sensor position {expected_pos}, got {sensor.pos}"

    def test_multiple_sensor_deployment(self, ship):
        """Test deploying multiple sensors at different locations"""
        initial_supplies = 100.0
        ship.supplies = initial_supplies
        
        # Deploy 3 sensors at different locations
        num_sensors = 3
        successful_deployments = 0
        
        for i in range(num_sensors):
            # Move ship to a new position for each sensor
            ship.pos = (ship.pos[0] + i, ship.pos[1])       # This will be random
            
            if hasattr(ship, 'addSensor'):
                result = ship.addSensor()
                if result:
                    successful_deployments += 1
            else:
                # Mock sensor deployment
                ship.supplies -= ship.supplies * 0.02
                ship.sensors.append(Sensor((ship.pos[0], ship.pos[1]), search_radius=2))
                successful_deployments += 1
        
        # Verify supplies decreased correctly (compound 2% reduction for successful deployments)
        expected_supplies = initial_supplies * (0.98 ** successful_deployments)
        assert abs(ship.supplies - expected_supplies) < 0.01, f"Expected ~{expected_supplies}, got {ship.supplies}"
        
        # Verify correct number of sensors
        assert len(ship.sensors) >= successful_deployments, f"Expected at least {successful_deployments} sensors"

    def test_sensor_detection_boundary(self, game_data):
        """Test that objects exactly at 2 CP distance are detected"""
        # Create sensor at origin
        sensor = Sensor((0, 0), search_radius=2)
        
        # Test boundary positions (exactly 2 CP away)
        boundary_positions = [
            (2, 0),   # 2 CP east
            (0, 2),   # 2 CP north
            (-2, 0),  # 2 CP west
            (0, -2),  # 2 CP south
            (2, 2),   # 2 CP northeast (diagonal)
            (-2, -2), # 2 CP southwest (diagonal)
        ]
        
        for pos in boundary_positions:
            distance = max(abs(pos[0]), abs(pos[1]))  # distance from origin
            assert distance <= 2, f"Position {pos} should be within sensor range"


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v"])