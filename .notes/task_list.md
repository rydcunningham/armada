# Armada Task List

This file tracks ongoing work, priorities, and notes. Update regularly as tasks progress or are completed.

---

## High Priority (In Progress / Immediate Attention)
1. **Set up Simpy skeleton**  
   - **Status**: Not started  
   - **Notes**: Create environment, initialize AAVs, and define basic processes (flight, dispatch).

2. **Integrate deck.gl visualization**  
   - **Status**: Not started  
   - **Notes**: Decide on front-end framework (Dash vs. Streamlit) and test with a simple map.

3. **Skyport & AAV Altitude Logic**  
   - **Status**: Not started  
   - **Notes**: Add `elevation_m` for Skyports and `altitude_m` for AAVs. Implement flight profile transitions (takeoff, cruise, landing).

---

## Medium Priority
1. **Real-Time Parameter Updates**  
   - **Status**: Planned  
   - **Notes**: Build a config object or dictionary that the front end can adjust without restarting the simulation.

2. **Battery Range & Charging Model**  
   - **Status**: Planned  
   - **Notes**: Hook in the Breguet range equation or stage-based consumption logic. Factor in charging times at Skyports.

3. **Analytics & Logging**  
   - **Status**: Planned  
   - **Notes**: Decide what stats to track (unfulfilled requests, average wait time, load factor, etc.) and how to display them in the UI.

---

## Low Priority
1. **Optimization Framework**  
   - **Status**: Future  
   - **Notes**: Possibly integrate a load-factor optimization engine or a solver to minimize unfulfilled requests or cost.

2. **Advanced Routing (Beyond Haversine)**  
   - **Status**: Future  
   - **Notes**: Replace simplified straight-line logic with a more complex route finding method, once the rest is stable.

3. **Documentation & Testing**  
   - **Status**: Ongoing  
   - **Notes**: Expand docstrings, write end-to-end tests. Might be escalated to Medium Priority as the project grows.

---

## Completed
- *(No tasks completed yet)*

