from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple
import math
from abc import ABC, abstractmethod

class VehicleState(Enum):
    """Base states common to all vehicles."""
    IDLE = auto()

class AAVState(VehicleState):
    """States specific to Autonomous Aerial Vehicles."""
    TAKEOFF = auto()
    CRUISE = auto()
    LANDING = auto()
    LANDED = auto()

class AGVState(VehicleState):
    """States specific to Autonomous Ground Vehicles."""
    EN_ROUTE_TO_RIDER = auto()
    ON_TRIP = auto()
    RETURNING_TO_BASE = auto()
    PARKED = auto()

@dataclass
class VehicleParams:
    """Base parameters for any vehicle."""
    max_speed_ms: float = 50.0  # meters per second

@dataclass
class FlightParams(VehicleParams):
    """Flight parameters specific to AAVs."""
    cruise_altitude_m: float = 300.0  # meters
    climb_rate_ms: float = 10.0  # meters per second
    descent_rate_ms: float = 5.0  # meters per second

class Vehicle(ABC):
    """Base class for all autonomous vehicles."""
    
    def __init__(self, vehicle_id: str, params: Optional[VehicleParams] = None):
        self.id = vehicle_id
        self.params = params or VehicleParams()
        self.state = VehicleState.IDLE
        self.current_location: Tuple[float, float] = (0.0, 0.0)  # lat, lon
        self.target_location: Optional[Tuple[float, float]] = None
        
    @abstractmethod
    def update_position(self, new_location: Tuple[float, float]) -> None:
        """Update the vehicle's position."""
        self.current_location = new_location
        
    @staticmethod
    def calculate_distance(loc1: Tuple[float, float], loc2: Tuple[float, float]) -> float:
        """Calculate distance between two points using Haversine formula."""
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        R = 6371000  # Earth's radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_phi/2) * math.sin(delta_phi/2) +
             math.cos(phi1) * math.cos(phi2) *
             math.sin(delta_lambda/2) * math.sin(delta_lambda/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
        
    def estimate_travel_time(self, from_loc: Tuple[float, float], to_loc: Tuple[float, float]) -> float:
        """Estimate travel time between two points in seconds."""
        distance = self.calculate_distance(from_loc, to_loc)
        return distance / self.params.max_speed_ms
        
    def __str__(self) -> str:
        return f"Vehicle {self.id} - State: {self.state.name} at ({self.current_location[0]}, {self.current_location[1]})"

class AAV(Vehicle):
    """Autonomous Aerial Vehicle with flight capabilities."""
    
    def __init__(self, vehicle_id: str, flight_params: Optional[FlightParams] = None):
        super().__init__(vehicle_id, flight_params or FlightParams())
        self.params: FlightParams = self.params  # Type hint for IDE support
        self.state: AAVState = AAVState.IDLE  # Start with AAV-specific state
        self.current_altitude_m: float = 0.0
        
    def update_position(self, new_location: Tuple[float, float], new_altitude: float = None) -> None:
        """Update the vehicle's position and optionally its altitude."""
        super().update_position(new_location)
        if new_altitude is not None:
            self.current_altitude_m = new_altitude
        
    def start_takeoff(self, from_location: Tuple[float, float]) -> None:
        """Begin takeoff sequence."""
        self.state = AAVState.TAKEOFF
        self.current_location = from_location
        
    def start_cruise(self, target_location: Tuple[float, float]) -> None:
        """Begin cruise phase towards target."""
        self.state = AAVState.CRUISE
        self.target_location = target_location
        self.current_altitude_m = self.params.cruise_altitude_m
        
    def start_landing(self) -> None:
        """Begin landing sequence."""
        self.state = AAVState.LANDING
        
    def complete_landing(self) -> None:
        """Complete landing sequence."""
        self.state = AAVState.LANDED
        self.current_altitude_m = 0.0
        
    def estimate_flight_time(self, from_loc: Tuple[float, float], to_loc: Tuple[float, float]) -> float:
        """Estimate total flight time between two points in seconds."""
        distance = self.calculate_distance(from_loc, to_loc)
        
        # Calculate phase times
        takeoff_time = self.params.cruise_altitude_m / self.params.climb_rate_ms
        cruise_time = distance / self.params.max_speed_ms
        landing_time = self.params.cruise_altitude_m / self.params.descent_rate_ms
        
        return takeoff_time + cruise_time + landing_time
        
    def __str__(self) -> str:
        return f"AAV {self.id} - State: {self.state.name} at ({self.current_location[0]}, {self.current_location[1]}, {self.current_altitude_m}m)" 