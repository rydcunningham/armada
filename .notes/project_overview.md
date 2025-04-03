# Project Overview: Armada

## Elevator Pitch

Armada is a real-time simulation platform for an autonomous aerial vehicle (AAV) network. We're starting with a minimal test network (2 skyports, 1 vehicle) to validate core trip logic and visualization before scaling up. The platform will eventually model Skyports (origin/destination hubs), AAV flight dynamics, Rider trip requests, and Dispatch algorithms, providing an interactive front-end for on-the-fly parameter changes and visualization.

## Development Phases

1. **Phase 1: Minimal Test Network**
   - 2 Skyports with basic landing pads
   - 1 AAV with simple flight dynamics
   - Basic trip logic between skyports
   - Simple visualization of vehicle movement

2. **Phase 2: Core Features**
   - Add multiple AAVs
   - Implement basic dispatch logic
   - Add rider requests
   - Expand to 3-5 skyports

3. **Phase 3: Advanced Features**
   - Full dispatch algorithms
   - Battery and charging systems
   - Complex routing
   - Analytics and optimization

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

## Data Storage Strategy

The analytics storage system is designed to be scalable and efficient:

1. **Test-Based Organization**
   - Each test scenario has its own directory (e.g., test_2_skyports_1_vehicle)
   - All related data (trips, vehicles, skyports) is grouped together
   - Makes it easy to track the complete state of a simulation run

2. **File Formats**
   - Raw data: JSON Lines format (one JSON object per line) for easy streaming
   - Processed data: Parquet format for efficient querying and storage
   - Metadata: JSON files for configuration and schema information

3. **Processing Pipeline**
   - Raw data is continuously written during simulation
   - Processors aggregate and transform data in batches
   - Aggregated data is optimized for dashboard queries

4. **Scalability Considerations**
   - Each test scenario is self-contained
   - Supports easy comparison between different test runs
   - Processed data can be moved to cold storage when old
   - Supports future migration to a proper time-series database if needed

## Key Technologies

- **Python (Simpy)**: Discrete-event simulation logic, manages entities (AAVs, Riders, Skyports).  
- **deck.gl**: Real-time 3D map visualization in the browser, showing flight paths and altitude changes.  
- **Dash or Streamlit**: Web framework for an interactive control panel + analytics dashboard.  
- **Jupyter Notebooks (optional)**: For prototyping or demonstration of simulation logic.

## Sample User Journeys

1. **Phase 1: Basic Vehicle Movement**
   - User opens the Armada dashboard
   - Sees a single AAV moving between two skyports
   - Can adjust basic parameters like speed and altitude
   - Visualizes the complete trip cycle

2. **Phase 2: Adding Complexity**
   - User adds more AAVs to the network
   - Implements basic dispatch logic
   - Tests with simple rider requests
   - Observes how the system handles multiple vehicles

3. **Phase 3: Full Network Analysis**
   - User adjusts load factors and wait times
   - Analyzes skyport capacity and charging needs
   - Tests battery range scenarios
   - Views comprehensive analytics
