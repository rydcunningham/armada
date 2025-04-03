# Armada Directory Structure

Below is an outline of how files and folders might be organized for collaboration and clarity.

```
armada/
├── config/
│   ├── settings.py      # Global constants and default config
│   ├── init.py
│   └── ...
├── data/
│   ├── sample/                   # Sample folder containing skyport infrastructure, routes, etc.
|   |   ├── sample_skyports.json  # Sample list of skyports with lat, lon, elevation
│   |   ├── sample_routes.json    # Optional test routes or adjacency data
│   |   ├── ...
│   └── ...
├── docs/
│   ├── project_overview.md   # High-level project goals & architecture
│   ├── task_list.md          # To-do list with priorities & statuses
│   ├── directory_structure.md
│   └── ...
├── sim/
│   ├── init.py
│   ├── entities.py          # Classes: Vehicles, Vehicles/AAV, Rider, Skyport, Battery
│   ├── dispatch.py          # Dispatch logic & matching functions
│   ├── flight_profiles.py   # Altitude/time logic (takeoff, cruise, landing)
│   ├── battery_model.py     # Battery consumption & Breguet equation
│   ├── simulation.py        # Main simpy environment & processes
│   └── ...
├── ui/
│   ├── app.py              # Dash/Streamlit main app
│   ├── deck_gl_layers.py   # Helpers for deck.gl layers & data transformations
│   ├── callbacks.py        # Functions that handle user interactions
│   └── ...
├── analytics/
│   ├── tests/
│   │   ├── test_2_skyports_1_vehicle/    # First test scenario
│   │   │   ├── raw/
│   │   │   │   ├── trip_requests.jsonl   # Raw trip request data
│   │   │   │   ├── vehicle_states.jsonl  # Raw vehicle state data
│   │   │   │   └── skyport_ops.jsonl     # Raw skyport operation data
│   │   │   └── processed/
│   │   │       ├── trip_metrics.parquet  # Processed trip metrics
│   │   │       ├── vehicle_metrics.parquet
│   │   │       └── skyport_metrics.parquet
│   │   ├── test_3_skyports_2_vehicles/   # Second test scenario
│   │   │   ├── raw/
│   │   │   └── processed/
│   │   └── ...
│   ├── processors/
│   │   ├── trip_processor.py     # Process and aggregate trip data
│   │   ├── vehicle_processor.py  # Process and aggregate vehicle data
│   │   └── skyport_processor.py  # Process and aggregate skyport data
│   └── utils/
│       ├── time_utils.py         # Time-based data processing utilities
│       └── aggregation.py        # Data aggregation functions
├── tests/
│   ├── test_entities.py    # Unit tests for AAV, Rider, etc.
│   ├── test_dispatch.py
│   ├── test_simulation.py
│   └── ...
├── .gitignore
└── README.md               # Basic overview & instructions
```

*Feel free to adapt the folder structure according to your workflows or constraints.*