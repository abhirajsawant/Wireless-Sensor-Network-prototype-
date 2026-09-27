# 🧠 ANN-Assisted Wireless Sensor Network

> **A research prototype for an energy-aware 3D Wireless Sensor Network (WSN) using LEACH-inspired clustering, Artificial Neural Networks (ANNs), MATLAB simulation, and Python-based visualization/application components.**

---

## 📌 Overview

This project explores an intelligent, energy-aware **3D Wireless Sensor Network** based on the clustering idea of **LEACH (Low-Energy Adaptive Clustering Hierarchy)**.

The project currently combines:

- **MATLAB** — main WSN simulation and algorithm development.
- **Python** — supporting application, data processing, and visualization.
- **Streamlit / Web UI** — presentation of simulation information and results.

The simulation uses two ANN stages:

```text
3D Sensor Nodes
      ↓
     ANN1
      ↓
Cluster Head (CH) Selection
      ↓
3D Distance-Based Clustering
      ↓
     ANN2
      ↓
Main Cluster Head (Main CH) Selection
      ↓
Communication
      ↓
Energy Update
      ↓
Next Round
```

---

## 🎯 Project Objective

The prototype investigates whether current network information can be used to make more energy-aware hierarchical decisions than basic probabilistic LEACH selection.

The main goals are to:

- Simulate a 3D WSN.
- Track residual energy of sensor nodes.
- Select Cluster Heads using ANN1.
- Form clusters using 3D distance.
- Select Main Cluster Heads using ANN2.
- Model TDMA-based intra-cluster communication.
- Model hierarchical communication toward the Base Station.
- Track network energy and node lifetime.
- Record CH and Main CH selections over simulation rounds.
- Provide Python/web-based visualization of the project data.

---

## 🏗️ Current Architecture

The project is not limited to MATLAB. MATLAB and Python serve different parts of the overall project.

```text
                    WSN Simulation
                         │
              ┌──────────┴──────────┐
              │                     │
           MATLAB                  Python
              │                     │
       Simulation / Logic      Processing / UI
              │                     │
              └──────────┬──────────┘
                         ↓
                Results / Data
                         ↓
             Streamlit / Web Interface
```

The exact separation of files may evolve as the project develops.

---

# 🧠 ANN-Based Selection

## ANN1 — Cluster Head Selection

ANN1 evaluates currently alive sensor nodes.

### Inputs

```text
1. X coordinate
2. Y coordinate
3. Z coordinate
4. Residual energy
5. Distance to Base Station
6. Average cluster energy
```

ANN1 produces a **CH suitability score**. Nodes with the highest scores are selected as Cluster Heads.

The prototype uses:

```text
p = 0.1
Number of CHs = max(1, floor(p × alive nodes))
```

---

## ANN2 — Main Cluster Head Selection

ANN2 evaluates the selected Cluster Heads.

### Inputs

```text
1. CH X coordinate
2. CH Y coordinate
3. CH Z coordinate
4. CH residual energy
5. CH distance to BS
6. Cluster size
```

ANN2 produces a **Main CH suitability score**.

The prototype uses:

```text
q = 0.1
Number of Main CHs = max(1, floor(q × number of CHs))
```

---

## ⚠️ Important: Current ANN Design

The current ANN implementation is a **prototype**, not a fully learned optimal policy.

The target values are generated using manually defined weighted functions.

### ANN1

```text
0.4 × Energy
+ 0.3 × Distance Suitability
+ 0.3 × Cluster Energy
```

### ANN2

```text
0.4 × Energy
+ 0.3 × Distance Suitability
+ 0.3 × Cluster Size Suitability
```

These weights are **prototype design choices** and should not be treated as values taken directly from a research paper unless separately verified.

---

# 🧩 Cluster Formation

After ANN1 selects the CHs, ordinary alive nodes are assigned to the **nearest CH using 3D Euclidean distance**.

```text
ANN1
 ↓
CH Selection
 ↓
3D Distance Calculation
 ↓
Nearest CH
 ↓
Cluster Assignment
```

Therefore, the current implementation should be described accurately as:

```text
ANN1 → CH selection
Distance → cluster membership
ANN2 → Main CH selection
```

Cluster sizes are naturally unequal because nodes are assigned according to their nearest CH.

---

# 📡 Communication Model

The current hierarchy is:

```text
Sensor Node
     │
     │ TDMA / local communication
     ↓
Cluster Head (CH)
     │
     ↓
Main Cluster Head (Main CH)
     │
     ↓
Base Station (BS)
```

The prototype models:

1. **Sensor Node → CH**
2. **CH → Main CH**
3. **Main CH → BS**

TDMA is represented as a logical scheduling mechanism for intra-cluster communication.

---

# ⚡ Energy Model

The current prototype uses a simplified radio-energy model.

Typical parameters include:

| Parameter | Default |
|---|---:|
| Sensor nodes | 100 |
| Network size | 100 × 100 × 100 m |
| Initial energy | 0.5 J |
| CH factor `p` | 0.1 |
| Main CH factor `q` | 0.1 |
| Packet length | 4000 bits |
| `ETX` | 50e-9 J/bit |
| `ERX` | 50e-9 J/bit |
| `Efs` | 10e-12 J/bit/m² |
| `EDA` | 5e-9 J/bit |

The prototype uses a free-space distance-squared transmission term:

```text
E_TX = L × ETX + L × Efs × d²
E_RX = L × ERX
```

Negative residual energy is clipped to zero.

---

# 🔄 Simulation Operation

The simulation operates dynamically rather than assuming a fixed lifetime.

Each round approximately follows:

```text
1. Find alive nodes
2. Update node information
3. Prepare ANN1 input
4. Predict ANN1 scores
5. Select CHs
6. Form clusters
7. Calculate cluster information
8. Prepare ANN2 input
9. Predict ANN2 scores
10. Select Main CHs
11. Assign TDMA slots
12. Node → CH communication
13. CH → Main CH communication
14. Main CH → BS communication
15. Update energy
16. Record round results
17. Continue until all nodes die
```

The simulation therefore determines the network lifetime from energy depletion instead of assuming beforehand that it will run for a fixed number of rounds.

---

# 📊 Recorded Results

The prototype records information such as:

- Alive nodes per round
- Dead nodes per round
- Total residual network energy
- First Node Death (FND)
- Half Node Death
- Last Node Death
- Total simulation rounds
- CH selection history
- Main CH selection history

### CH History

The simulation can preserve which nodes were selected in each round.

```text
Round 1 → CH IDs
Round 2 → CH IDs
Round 3 → CH IDs
...
```

The same concept is used for Main CH selections.

This allows analysis of CH rotation and how often individual nodes receive higher-level roles.

---

# 🖥️ MATLAB + Python

## MATLAB

MATLAB is used for the core simulation work, including:

- 3D node deployment
- Network rounds
- ANN1 / ANN2 processing
- CH selection
- Main CH selection
- Cluster formation
- Communication
- Energy consumption
- Network lifetime
- Simulation plots

## Python

Python is used as part of the project for the application/data side of the system, including the project's visualization and interface components.

The Python side is intended to make simulation information easier to inspect and present rather than replacing the underlying WSN research logic.

---

# 🌐 Visualization / Interface

The project also contains a web/application layer for presenting the simulation.

The overall idea is:

```text
MATLAB / Python Simulation Data
             ↓
       Data Processing
             ↓
     ┌───────┴────────┐
     ↓                ↓
 Streamlit       Web Frontend
                    │
              HTML / CSS / JS
```

This allows the research simulation and the user-facing visualization to remain separate.

---

# 📈 Current Metrics

Currently emphasized:

- Network lifetime
- FND
- Half Node Death
- Last Node Death
- Alive/dead nodes
- Residual energy
- CH selection
- Main CH selection

Potential future metrics include:

- Throughput
- Packet Delivery Ratio (PDR)
- End-to-end delay
- Energy efficiency
- Control overhead
- Energy variance
- CH selection frequency

---

# ⚠️ Current Limitations

This repository should currently be considered a **research prototype**.

Important limitations include:

- ANN targets are manually constructed.
- ANN1 and ANN2 are trained using the prototype target functions.
- The ANNs are not retrained every round.
- Cluster membership is distance-based rather than directly ANN-based.
- The radio-energy model is simplified.
- Link quality is not currently a direct ANN feature.
- Packet-level reliability and retransmissions are not fully modeled.
- Throughput, PDR, and delay are not yet fully implemented.
- A single simulation run is not sufficient for strong experimental validation.

These limitations should be considered when interpreting simulation results.

---

# 🧪 Experimental Evaluation

For research comparisons, experiments should use consistent:

```text
Node count
Network dimensions
BS position
Initial energy
Packet size
Energy model
Deployment conditions
Termination condition
Number of independent runs
```

Multiple random seeds/runs should be used when producing final performance claims.

For reproducibility, MATLAB can use a fixed seed such as:

```matlab
rng(1);
```

---

# 🚀 Future Direction

Possible extensions include:

```text
Current Prototype
      ↓
Better ANN Training Data
      ↓
Link-Quality Features
      ↓
Improved Cluster Membership
      ↓
Multi-Hop Routing
      ↓
Throughput / PDR / Delay
      ↓
Statistical Validation
```

Other possible research directions include:

- Optimization-generated ANN labels
- Larger simulation datasets
- Online learning
- Reinforcement learning
- Load-aware routing
- Energy-aware multi-hop routing
- More detailed communication models

---

# 📚 Research Position

The project combines ideas from:

- LEACH and hierarchical WSN protocols
- Energy-aware clustering
- Artificial Neural Networks
- 3D wireless sensor network simulation
- Hierarchical routing
- Network lifetime analysis
- Python-based data visualization/application development

The repository should clearly distinguish between:

1. **Literature-derived concepts**
2. **Prototype design decisions**
3. **Simulation assumptions**
4. **Measured results**
5. **Future research extensions**

---

# 📁 Project Structure

The repository contains multiple parts of the project rather than being only a MATLAB simulation.

Conceptually:

```text
Wireless Sensor Network
│
├── MATLAB
│   └── WSN simulation / ANN / energy model
│
├── Python
│   └── application / processing / visualization
│
├── Web Interface
│   └── HTML / CSS / JavaScript
│
├── Streamlit
│   └── interactive presentation
│
└── Documentation / Results
```

The exact filenames and folders should be kept consistent with the current repository implementation.

---

# ▶️ Running the Project

### MATLAB

Open the MATLAB portion of the repository and run the main simulation script.

The simulation should:

```text
Deploy nodes
   ↓
Run ANN-based selection
   ↓
Form clusters
   ↓
Communicate
   ↓
Consume energy
   ↓
Repeat rounds
   ↓
Generate results
```

### Python / Web Components

Use the Python environment and dependencies provided by the repository to run the corresponding application or visualization components.

The Python/web layer is intended for working with and presenting the simulation rather than changing the core WSN methodology.

---

# 📖 Terminology

| Term | Meaning |
|---|---|
| WSN | Wireless Sensor Network |
| LEACH | Low-Energy Adaptive Clustering Hierarchy |
| ANN | Artificial Neural Network |
| CH | Cluster Head |
| Main CH | Main Cluster Head |
| BS | Base Station |
| TDMA | Time Division Multiple Access |
| FND | First Node Death |
| PDR | Packet Delivery Ratio |

---

# 📌 Summary

The current project is an **ANN-assisted 3D WSN research prototype** combining MATLAB simulation with Python/application components.

The main decision hierarchy is:

```text
3D Sensor Nodes
      ↓
     ANN1
      ↓
     CHs
      ↓
3D Distance-Based Clustering
      ↓
     ANN2
      ↓
   Main CHs
      ↓
Node → CH → Main CH → BS
      ↓
Energy Update
      ↓
Network Lifetime
```

The purpose of the repository is to provide a working foundation for experimenting with intelligent, energy-aware WSN clustering and routing while allowing the results to be explored through Python/web-based interfaces.
