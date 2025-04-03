from typing import Dict, List, Tuple, Optional, Type
import simpy
import numpy as np
from .entities.skyport import Skyport, SkyportLocation
from .entities.vehicle import Vehicle, AAV, VehicleState, AAVState, FlightParams

class ArmadaSimulation:
    """Main simulation environment for the Armada system."""
    
    def __init__(self, env: Optional[simpy.Environment] = None):
        self.env = env or simpy.Environment()
        self.skyports: Dict[str, Skyport] = {}
        self.vehicles: Dict[str, Vehicle] = {}  # Now stores any Vehicle type
        self.flight_states: Dict[str, List[Tuple[float, Tuple[float, float], float]]] = {}  # vehicle_id -> [(time, (lat, lon), altitude)]
        
    def add_skyport(self, name: str, lat: float, lon: float, elevation_m: float, num_pads: int = 1) -> None:
        """Add a skyport to the simulation."""
        location = SkyportLocation(lat=lat, lon=lon, elevation_m=elevation_m, name=name)
        self.skyports[name] = Skyport(location, num_pads)
        
    def add_vehicle(self, vehicle_id: str, vehicle_type: Type[Vehicle] = AAV, 
                   params: Optional[FlightParams] = None) -> None:
        """Add a vehicle to the simulation."""
        self.vehicles[vehicle_id] = vehicle_type(vehicle_id, params)
        self.flight_states[vehicle_id] = []
        
    def interpolate_position(self, start: Tuple[float, float], end: Tuple[float, float], 
                           progress: float) -> Tuple[float, float]:
        """Linearly interpolate between two points based on progress (0-1)."""
        return (
            start[0] + (end[0] - start[0]) * progress,
            start[1] + (end[1] - start[1]) * progress
        )
        
    def vehicle_process(self, vehicle: AAV, from_port: str, to_port: str) -> simpy.Process:
        """Simulate a vehicle's flight from one skyport to another."""
        
        def flight_process(env: simpy.Environment) -> simpy.Process:
            # Get skyport locations
            start_port = self.skyports[from_port]
            end_port = self.skyports[to_port]
            
            # Request landing pad at destination
            while not end_port.request_landing(vehicle.id):
                yield env.timeout(10)  # Wait and try again
            
            # Start takeoff
            start_loc = (start_port.location.lat, start_port.location.lon)
            end_loc = (end_port.location.lat, end_port.location.lon)
            
            vehicle.start_takeoff(start_loc)
            start_port.takeoff_vehicle(vehicle.id)
            
            # Takeoff phase
            takeoff_time = vehicle.params.cruise_altitude_m / vehicle.params.climb_rate_ms
            steps = int(takeoff_time)
            for i in range(steps):
                altitude = (i + 1) * vehicle.params.climb_rate_ms
                self.flight_states[vehicle.id].append(
                    (env.now + i, start_loc, altitude)
                )
                yield env.timeout(1)
                
            # Start cruise
            vehicle.start_cruise(end_loc)
            distance = vehicle.calculate_distance(start_loc, end_loc)
            cruise_time = distance / vehicle.params.max_speed_ms
            steps = int(cruise_time)
            
            for i in range(steps):
                progress = (i + 1) / steps
                current_pos = self.interpolate_position(start_loc, end_loc, progress)
                self.flight_states[vehicle.id].append(
                    (env.now + i, current_pos, vehicle.params.cruise_altitude_m)
                )
                yield env.timeout(1)
                
            # Landing phase
            vehicle.start_landing()
            landing_time = vehicle.params.cruise_altitude_m / vehicle.params.descent_rate_ms
            steps = int(landing_time)
            
            for i in range(steps):
                altitude = vehicle.params.cruise_altitude_m - (i + 1) * vehicle.params.descent_rate_ms
                self.flight_states[vehicle.id].append(
                    (env.now + i, end_loc, max(0, altitude))
                )
                yield env.timeout(1)
                
            # Complete landing
            vehicle.complete_landing()
            end_port.land_vehicle(vehicle.id)
            self.flight_states[vehicle.id].append(
                (env.now, end_loc, 0)
            )
            
        return self.env.process(flight_process(self.env))
        
    def get_vehicle_states(self) -> Dict[str, List[Tuple[float, Tuple[float, float], float]]]:
        """Get the current state of all vehicles for visualization."""
        return self.flight_states
        
    def get_skyport_locations(self) -> List[Dict]:
        """Get skyport locations for visualization."""
        return [
            {
                "name": name,
                "location": [port.location.lon, port.location.lat],  # GeoJSON format
                "elevation": port.location.elevation_m
            }
            for name, port in self.skyports.items()
        ] 