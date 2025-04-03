from dash import Dash, html
from dash.dependencies import Input, Output
import dash_deck
import pydeck as pdk
import numpy as np
from sim.simulation import ArmadaSimulation
import simpy

# Initialize simulation with two skyports
sim = ArmadaSimulation()

# Add two skyports (using San Francisco and Oakland as example locations)
sim.add_skyport("SFO", 37.7749, -122.4194, 4.0)  # San Francisco
sim.add_skyport("OAK", 37.8044, -122.2712, 3.0)  # Oakland

# Add one vehicle
sim.add_vehicle("AAV001")

# Start a flight from SFO to OAK
sim.vehicle_process(sim.vehicles["AAV001"], "SFO", "OAK")

# Run simulation for initial state
sim.env.run(until=1)

# Initialize Dash app
app = Dash(__name__)

def create_deck():
    """Create the deck.gl visualization."""
    # Get current vehicle states and skyport locations
    vehicle_states = sim.get_vehicle_states()
    skyports = sim.get_skyport_locations()
    
    # Create layers
    layers = []
    
    # Skyport layer
    skyport_layer = pdk.Layer(
        "ScatterplotLayer",
        data=skyports,
        get_position="location",
        get_fill_color=[255, 140, 0],
        get_radius=100,
        pickable=True,
    )
    layers.append(skyport_layer)
    
    # Vehicle layer (if we have states)
    for vehicle_id, states in vehicle_states.items():
        if states:
            latest_state = states[-1]
            vehicle_layer = pdk.Layer(
                "ScatterplotLayer",
                data=[{
                    "position": [latest_state[1][1], latest_state[1][0]],  # [lon, lat]
                    "elevation": latest_state[2]
                }],
                get_position="position",
                get_fill_color=[66, 135, 245],
                get_radius=50,
                pickable=True,
            )
            layers.append(vehicle_layer)
            
            # Add path layer for vehicle trail
            path_data = [{
                "path": [[state[1][1], state[1][0], state[2]] for state in states[-20:]]  # Last 20 positions
            }]
            path_layer = pdk.Layer(
                "PathLayer",
                data=path_data,
                get_path="path",
                get_width=5,
                get_color=[66, 135, 245],
            )
            layers.append(path_layer)
    
    # Create view state centered between the skyports
    view_state = pdk.ViewState(
        latitude=37.7896,  # Midpoint between SF and Oakland
        longitude=-122.3453,
        zoom=11,
        pitch=45,
    )
    
    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style="dark",
    )

app.layout = html.Div([
    html.H1("Armada Simulation"),
    dash_deck.DeckGL(
        id='deck-gl',
        data=create_deck().to_json(),
        style={'height': '800px'},
    ),
    html.Button('Step Simulation', id='step-button', n_clicks=0),
])

@app.callback(
    Output('deck-gl', 'data'),
    Input('step-button', 'n_clicks')
)
def update_simulation(n_clicks):
    """Step the simulation forward and update visualization."""
    if n_clicks > 0:
        sim.env.run(until=sim.env.now + 10)  # Run for 10 more seconds
    return create_deck().to_json()

if __name__ == '__main__':
    app.run_server(debug=True) 