# Project Overview: Armada

## Elevator Pitch

Armada is a real-time simulation platform for an autonomous aerial vehicle (AAV) network. It models Skyports (origin/destination hubs), AAV flight dynamics, Rider trip requests, and Dispatch algorithms, providing an interactive front-end for on-the-fly parameter changes and visualization. Our goal is to allow planners, engineers, or analysts to tweak flight, dispatch, and charging parameters in real time and see network-wide effects immediately.

## High-Level Architecture

1. **Simulation Engine (Backend)**
   - **Language & Framework**: Python + Simpy for discrete-event simulation.
   - **Core Components**:  
     - AAV classes (tracks altitude, battery status, seats).  
     - Skyport classes (manages landing pads, chargers, hangar capacity).  
     - Dispatch logic (load factor, max wait times).  
     - Logging and analytics (Trip_History, usage stats).

2. **Visualization Layer (Frontend)**
   - **Deck.gl** (for 3D geospatial rendering of AAV flights and skyports).
   - **UI Framework**: Potentially Dash, Streamlit, or another web-based Python tool to house controls (parameter editing) and analytics panels.

3. **Communication / Data Flow**
   - Front-end communicates new parameters (e.g., load factor, wait time) to the Python backend.  
   - The simulation engine processes these updates without restarting.  
   - The deck.gl view (via the chosen UI layer) refreshes to display updated AAV positions, statuses, and analytics.

## Key Technologies

- **Python (Simpy)**: Discrete-event simulation logic, manages entities (AAVs, Riders, Skyports).  
- **deck.gl**: Real-time 3D map visualization in the browser, showing flight paths and altitude changes.  
- **Dash or Streamlit**: Web framework for an interactive control panel + analytics dashboard.  
- **Jupyter Notebooks (optional)**: For prototyping or demonstration of simulation logic.

## Sample User Journeys

1. **Planner Adjusts Load Factor**  
   - The planner opens the Armada dashboard.  
   - From the side panel, they increase the load factor threshold (e.g., from 50% to 70%).  
   - The back-end simulation updates how Dispatch assigns riders to AAVs in real time, reducing the overall number of flights but slightly increasing wait times.  
   - The 3D visualization shows fewer AAVs departing, with more seats filled on each flight.

2. **Analyzing Skyport Capacity**  
   - A user sees frequent congestion at a particular Skyport.  
   - They increase the number of landing pads (or fast chargers) in the side panel.  
   - The simulation re-runs ongoing events with immediate effect, showing improved turnaround times and decreased queue lengths.  
   - The user checks the analytics panel to confirm shorter wait times and fewer unfulfilled requests.

3. **Battery Range Experiment**  
   - The user changes the battery capacity of all AAV models from 300 kWh to 250 kWh.  
   - New flights in the simulation have shorter maximum range, leading to more frequent charging stops.  
   - The user sees how wait times, route planning, and unfulfilled rides change as a result.
