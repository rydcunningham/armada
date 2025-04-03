from dataclasses import dataclass
from typing import Optional, List

@dataclass
class SkyportLocation:
    """Geographic location and elevation of a Skyport."""
    lat: float
    lon: float
    elevation_m: float
    name: str

class Skyport:
    """A Skyport facility that can handle AAV landings and takeoffs."""
    
    def __init__(self, location: SkyportLocation, num_pads: int = 1):
        self.location = location
        self.num_pads = num_pads
        self.available_pads = num_pads  # Initially all pads are available
        self.landed_vehicles: List[str] = []  # List of vehicle IDs currently at this skyport
        
    def request_landing(self, vehicle_id: str) -> bool:
        """Attempt to reserve a landing pad."""
        if self.available_pads > 0:
            self.available_pads -= 1
            return True
        return False
        
    def land_vehicle(self, vehicle_id: str) -> None:
        """Record a vehicle as landed at this skyport."""
        self.landed_vehicles.append(vehicle_id)
        
    def takeoff_vehicle(self, vehicle_id: str) -> None:
        """Record a vehicle as taking off from this skyport."""
        if vehicle_id in self.landed_vehicles:
            self.landed_vehicles.remove(vehicle_id)
            self.available_pads += 1
            
    def __str__(self) -> str:
        return f"Skyport {self.location.name} at ({self.location.lat}, {self.location.lon})" 