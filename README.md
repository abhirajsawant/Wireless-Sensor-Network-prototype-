# 🧠 Artificial Neural Network-Assisted 3D Wireless Sensor Network

> **An Artificial Neural Network (ANN)-assisted energy-aware clustering and hierarchical routing framework for a three-dimensional Wireless Sensor Network (WSN).**

---

## 📌 Overview

This project is a MATLAB-based research prototype for an intelligent, energy-aware **three-dimensional (3D) Wireless Sensor Network (WSN)**.

The framework is inspired by the clustering concept of **Low-Energy Adaptive Clustering Hierarchy (LEACH)** and extends the basic clustering architecture by introducing two **Artificial Neural Network (ANN)** stages:

1. **Artificial Neural Network 1 (ANN1)**  
   Evaluates the current condition of alive sensor nodes and generates a suitability score for **Cluster Head (CH)** selection.

2. **Artificial Neural Network 2 (ANN2)**  
   Evaluates the selected Cluster Heads (CHs) and generates a suitability score for **Main Cluster Head (Main CH)** selection.

The communication hierarchy is:

```text
Sensor Nodes
     │
     │ Time Division Multiple Access (TDMA)
     ▼
Cluster Heads (CHs)
     │
     │ Scheduled / hierarchical communication
     ▼
Main Cluster Head(s) (Main CH)
     │
     │ Long-range transmission
     ▼
Base Station (BS)
```

The simulation operates dynamically in rounds. At every round, the current network condition is evaluated and new Cluster Heads (CHs) and Main Cluster Heads (Main CHs) can be selected.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Project Status](#-project-status)
- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Proposed Architecture](#-proposed-architecture)
- [Complete System Workflow](#-complete-system-workflow)
- [Network Model](#-network-model)
- [Sensor Node Model](#-sensor-node-model)
- [Node Information Packet](#-node-information-packet)
- [Artificial Neural Network 1](#-artificial-neural-network-1-ann1)
- [Cluster Head Selection](#-cluster-head-selection)
- [Cluster Formation](#-cluster-formation)
- [Cluster Size and Average Cluster Energy](#-cluster-size-and-average-cluster-energy)
- [Artificial Neural Network 2](#-artificial-neural-network-2-ann2)
- [Main Cluster Head Selection](#-main-cluster-head-selection)
- [Time Division Multiple Access](#-time-division-multiple-access-tdma)
- [Communication Architecture](#-communication-architecture)
- [Energy Model](#-energy-model)
- [Dynamic Round Operation](#-dynamic-round-operation)
- [Round-by-Round CH and Main CH History](#-round-by-round-ch-and-main-ch-history)
- [Network Lifetime](#-network-lifetime)
- [Visualization](#-visualization)
- [Parameters](#-parameters)
- [Variable Reference](#-variable-reference)
- [Algorithm Pseudocode](#-algorithm-pseudocode)
- [MATLAB Implementation](#-matlab-implementation)
- [How to Run](#-how-to-run)
- [Debugging](#-debugging)
- [Reproducibility](#-reproducibility)
- [Experimental Methodology](#-experimental-methodology)
- [Baseline Comparison](#-baseline-comparison)
- [Statistical Evaluation](#-statistical-evaluation)
- [Current Limitations](#-current-limitations)
- [Future Improvements](#-future-improvements)
- [Research Notes](#-research-notes)
- [Terminology](#-terminology)
- [License](#-license)

---

# 📌 Project Status

This repository represents a **research prototype / simulation framework**.

The current implementation is intended to establish and test the complete simulation pipeline:

```text
3D deployment
    ↓
ANN1
    ↓
CH selection
    ↓
Cluster formation
    ↓
ANN2
    ↓
Main CH selection
    ↓
Communication
    ↓
Energy update
    ↓
Next round
```

### Important interpretation

The current implementation should **not** automatically be considered a finalized or experimentally validated protocol.

In particular:

- ANN1 uses a manually constructed prototype target function.
- ANN2 uses a manually constructed prototype target function.
- Ordinary-node cluster membership is currently based on nearest-CH 3D distance.
- ANN1 and ANN2 are trained once and reused during the dynamic simulation.
- The current radio-energy model is a simplified prototype.
- Throughput, Packet Delivery Ratio (PDR), and end-to-end delay are not yet fully implemented.
- Statistical validation requires multiple independent simulation runs.

---

# 🎯 Problem Statement

Traditional **Low-Energy Adaptive Clustering Hierarchy (LEACH)** improves energy efficiency by organizing sensor nodes into clusters and rotating the Cluster Head (CH) role.

However, conventional clustering can suffer from:

- Unequal energy consumption.
- Unequal communication distances.
- Overloaded Cluster Heads (CHs).
- Premature depletion of low-energy nodes.
- Long-distance communication between Cluster Heads (CHs) and the Base Station (BS).
- Selection mechanisms that do not jointly consider all current network conditions.

The proposed framework investigates an intelligent hierarchy in which:

```text
Current node condition
        ↓
Artificial Neural Network (ANN)
        ↓
Suitability score
        ↓
Cluster Head (CH)
```

and then:

```text
Current CH condition
        ↓
Artificial Neural Network (ANN)
        ↓
Suitability score
        ↓
Main Cluster Head (Main CH)
```

---

# 🎯 Objectives

The main objectives of the prototype are:

1. Build a 3D Wireless Sensor Network (WSN) simulation.
2. Represent every sensor node using X, Y, and Z coordinates.
3. Track residual energy dynamically.
4. Calculate 3D communication distances.
5. Use Artificial Neural Network 1 (ANN1) for Cluster Head (CH) selection.
6. Use Artificial Neural Network 2 (ANN2) for Main Cluster Head (Main CH) selection.
7. Allow Cluster Head (CH) counts to change according to the number of alive nodes.
8. Allow Main Cluster Head (Main CH) counts to change according to the number of Cluster Heads (CHs).
9. Form unequal clusters.
10. Simulate hierarchical communication.
11. Model Time Division Multiple Access (TDMA) scheduling.
12. Update residual energy after communication.
13. Continue simulation until all nodes are dead.
14. Record network lifetime.
15. Record Cluster Head (CH) and Main Cluster Head (Main CH) selection history.
16. Visualize the final 3D network state.

---

# 🏗️ Proposed Architecture

## High-Level Architecture

```text
                    ┌───────────────────────┐
                    │   3D Sensor Nodes     │
                    │       (WSN)           │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      ANN1             │
                    │ CH Suitability        │
                    │ Evaluation             │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Cluster Heads       │
                    │        (CHs)          │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Cluster Formation   │
                    │    3D Distance Based  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      ANN2             │
                    │ Main CH Suitability   │
                    │ Evaluation             │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Main CH(s)        │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Base Station       │
                    │         (BS)          │
                    └───────────────────────┘
```

---

# 🔄 Complete System Workflow

The complete simulation flow is:

```text
START
  │
  ▼
Initialize MATLAB
  │
  ▼
Define WSN parameters
  │
  ▼
Deploy sensor nodes randomly in 3D
  │
  ▼
Define Base Station (BS)
  │
  ▼
Calculate initial node-to-BS distances
  │
  ▼
Calculate initial average energy
  │
  ▼
Create NodeInfo_Packet
  │
  ▼
Prepare ANN1
  │
  ▼
Train ANN1
  │
  ▼
Prepare ANN2
  │
  ▼
Train ANN2
  │
  ▼
Start simulation
  │
  ▼
Find alive nodes
  │
  ▼
Update distances
  │
  ▼
Build current ANN1 input
  │
  ▼
Normalize ANN1 input
  │
  ▼
ANN1 prediction
  │
  ▼
Select Cluster Heads (CHs)
  │
  ▼
Form clusters
  │
  ▼
Calculate cluster sizes
  │
  ▼
Calculate average cluster energy
  │
  ▼
Update CH information
  │
  ▼
Build ANN2 input
  │
  ▼
Normalize ANN2 input
  │
  ▼
ANN2 prediction
  │
  ▼
Select Main Cluster Head(s)
  │
  ▼
Assign TDMA slots
  │
  ▼
Sensor Node → CH
  │
  ▼
CH → Main CH
  │
  ▼
Main CH → BS
  │
  ▼
Update residual energy
  │
  ▼
Record round results
  │
  ▼
Are nodes alive?
  │
  ├──────── YES ────────► Next round
  │
  └──────── NO ─────────► Final results
                              │
                              ▼
                         Plot results
                              │
                              ▼
                            END
```

---

# 📐 Network Model

The simulation uses a three-dimensional deployment area.

Default dimensions:

| Parameter | Value |
|---|---:|
| X dimension | 100 m |
| Y dimension | 100 m |
| Z dimension | 100 m |

Every sensor node has:

```text
X coordinate
Y coordinate
Z coordinate
```

The default Base Station (BS) position is:

```text
BS = (50, 50, 0)
```

---

# 📍 3D Distance Model

For two points:

```text
A = (x₁, y₁, z₁)
B = (x₂, y₂, z₂)
```

the 3D Euclidean distance is:

```text
d = √[(x₁-x₂)² + (y₁-y₂)² + (z₁-z₂)²]
```

MATLAB:

```matlab
distance = sqrt( ...
    (x1-x2)^2 + ...
    (y1-y2)^2 + ...
    (z1-z2)^2);
```

The same 3D distance concept is used for:

- Sensor Node → Base Station (BS)
- Sensor Node → Cluster Head (CH)
- Cluster Head (CH) → Main Cluster Head (Main CH)
- Main Cluster Head (Main CH) → Base Station (BS)

---

# 📦 Sensor Node Model

Each sensor node is represented using a MATLAB structure.

Important fields:

```matlab
node(i).x
node(i).y
node(i).z
node(i).energy
node(i).distanceBS
node(i).avgClusterEnergy
node(i).CH_x
node(i).CH_y
node(i).CH_z
node(i).isCH
node(i).isMainCH
```

## Field Description

| Field | Description |
|---|---|
| `x` | X coordinate |
| `y` | Y coordinate |
| `z` | Z coordinate |
| `energy` | Current residual energy |
| `distanceBS` | 3D distance to Base Station (BS) |
| `avgClusterEnergy` | Average residual energy of the node's current cluster |
| `CH_x` | X coordinate of serving Cluster Head (CH) |
| `CH_y` | Y coordinate of serving Cluster Head (CH) |
| `CH_z` | Z coordinate of serving Cluster Head (CH) |
| `isCH` | Indicates current Cluster Head (CH) status |
| `isMainCH` | Indicates current Main Cluster Head (Main CH) status |

---

# 🔢 Main Simulation Parameters

The default prototype uses:

```matlab
SN = 100;

area_x = 100;
area_y = 100;
area_z = 100;

Eo = 0.5;

BS.x = 50;
BS.y = 50;
BS.z = 0;
```

---

# 📦 Node Information Packet

The complete node information packet contains **nine features**.

```text
┌───────┬───────────────────────────────┐
│ Index │ Feature                       │
├───────┼───────────────────────────────┤
│   1   │ Sensor X                      │
│   2   │ Sensor Y                      │
│   3   │ Sensor Z                      │
│   4   │ Current residual energy       │
│   5   │ Distance to BS                │
│   6   │ Average cluster energy        │
│   7   │ CH X                          │
│   8   │ CH Y                          │
│   9   │ CH Z                          │
└───────┴───────────────────────────────┘
```

MATLAB:

```matlab
NodeInfo_Packet = zeros(SN,9);

for i = 1:SN
    NodeInfo_Packet(i,1) = node(i).x;
    NodeInfo_Packet(i,2) = node(i).y;
    NodeInfo_Packet(i,3) = node(i).z;
    NodeInfo_Packet(i,4) = node(i).energy;
    NodeInfo_Packet(i,5) = node(i).distanceBS;
    NodeInfo_Packet(i,6) = node(i).avgClusterEnergy;
    NodeInfo_Packet(i,7) = node(i).CH_x;
    NodeInfo_Packet(i,8) = node(i).CH_y;
    NodeInfo_Packet(i,9) = node(i).CH_z;
end
```

Dimensions:

```text
SN × 9
```

For 100 nodes:

```text
100 × 9
```

---

# 🧠 Artificial Neural Network 1 (ANN1)

ANN1 is responsible for **Cluster Head (CH) selection**.

## ANN1 Question

ANN1 effectively answers:

> Which currently alive sensor nodes have higher suitability to become Cluster Heads (CHs)?

---

## ANN1 Inputs

ANN1 receives six inputs:

```text
1. X coordinate
2. Y coordinate
3. Z coordinate
4. Current residual energy
5. Distance to Base Station (BS)
6. Average cluster energy
```

MATLAB:

```matlab
ANN1_Input = X(:,1:6);
```

Dimensions:

```text
SN × 6
```

---

# ❗ Why ANN1 Does Not Use CH Coordinates

The complete Node Information Packet has:

```text
CH_X
CH_Y
CH_Z
```

but these cannot be used as first-stage inputs because the Cluster Head (CH) is not known yet.

The dependency is:

```text
ANN1
 ↓
CH selection
 ↓
CH becomes known
 ↓
CH coordinates available
```

Therefore:

```text
ANN1 = first 6 features
```

and:

```text
CH_X, CH_Y, CH_Z
```

are populated after Cluster Head (CH) selection.

This avoids a circular dependency.

---

# 📊 ANN1 Input Normalization

The prototype uses min-max normalization:

```text
Normalized Value =
(Value - Minimum) / (Maximum - Minimum)
```

MATLAB:

```matlab
inputMin = min(ANN1_Input);
inputMax = max(ANN1_Input);
inputRange = inputMax - inputMin;

ANN1_Input_Norm = zeros(size(ANN1_Input));

for j = 1:6
    if inputRange(j) == 0
        ANN1_Input_Norm(:,j) = 0.5;
    else
        ANN1_Input_Norm(:,j) = ...
            (ANN1_Input(:,j) - inputMin(j)) ...
            / inputRange(j);
    end
end
```

If the minimum and maximum values are equal, the feature has no variation.

The prototype assigns:

```text
0.5
```

to avoid division by zero.

---

# 🎯 ANN1 Prototype Target

The current prototype uses a manually designed suitability target.

The three components are:

```matlab
energyScore = ANN1_Input_Norm(:,4);
distanceScore = 1 - ANN1_Input_Norm(:,5);
clusterEnergyScore = ANN1_Input_Norm(:,6);
```

The target is:

```matlab
ANN1_Target = ...
    0.4 * energyScore + ...
    0.3 * distanceScore + ...
    0.3 * clusterEnergyScore;
```

Therefore:

```text
ANN1 Target =
0.4 × Energy Suitability
+
0.3 × Distance Suitability
+
0.3 × Cluster Energy Suitability
```

### Important

The `0.4`, `0.3`, and `0.3` weights are **prototype design choices**.

They should not be described as values directly taken from a reference paper unless separately verified.

The current ANN1 therefore learns to approximate a manually constructed suitability function.

---

# 🏗️ ANN1 Architecture

The prototype uses:

```matlab
hiddenNeurons = 10;
net1 = feedforwardnet(hiddenNeurons);
```

Conceptually:

```text
6 Inputs
   │
   ▼
10 Hidden Neurons
   │
   ▼
1 Suitability Score
```

Training:

```matlab
ANN1_Input_Train = ANN1_Input_Norm';
ANN1_Target_Train = ANN1_Target';

net1 = train( ...
    net1, ...
    ANN1_Input_Train, ...
    ANN1_Target_Train);
```

Prediction:

```matlab
ANN1_Output = net1(ANN1_Input_Train)';
```

---

# 👑 Cluster Head (CH) Selection

The Cluster Head (CH) growth factor is:

```matlab
p = 0.1;
```

The number of Cluster Heads is:

```matlab
numberOfCH = floor(p * aliveNodes);
numberOfCH = max(1,numberOfCH);
```

### Example

If:

```text
Alive Nodes = 100
p = 0.1
```

then:

```text
0.1 × 100 = 10
```

so:

```text
10 Cluster Heads
```

If:

```text
Alive Nodes = 37
```

then:

```text
0.1 × 37 = 3.7
floor(3.7) = 3
```

so:

```text
3 Cluster Heads
```

---

# 🏆 Selecting the Highest ANN1 Scores

ANN1 outputs are sorted:

```matlab
[sortedScores, sortedIndex] = ...
    sort(ANN1_Output,'descend');
```

The top nodes are selected:

```matlab
CH_Index = alive(sortedIndex(1:numberOfCH));
```

The process is:

```text
Alive Nodes
     ↓
ANN1
     ↓
Suitability Scores
     ↓
Sort Descending
     ↓
Select Top Nodes
     ↓
Cluster Heads
```

---

# 🔄 Dynamic Cluster Head Rotation

Cluster Head (CH) selection is performed again in every simulation round.

A node can therefore:

```text
Round 1 → CH
Round 2 → Normal Node
Round 3 → CH
Round 4 → Normal Node
```

The previous role is not directly used as an ANN1 label.

The current network state is reevaluated.

---

# 🧩 Cluster Formation

After Cluster Head (CH) selection, ordinary alive nodes are assigned to a Cluster Head (CH).

The current implementation uses:

> **Nearest Cluster Head based on 3D Euclidean distance.**

For every ordinary node, the distance to every selected Cluster Head (CH) is calculated.

```matlab
distanceToCH(j) = sqrt( ...
    (node(i).x - CH_x(j))^2 + ...
    (node(i).y - CH_y(j))^2 + ...
    (node(i).z - CH_z(j))^2);
```

The closest Cluster Head (CH) is selected:

```matlab
[~,nearestCH] = min(distanceToCH);
```

---

# ⚠️ Important Cluster Formation Note

The current implementation is:

```text
ANN1 → selects CHs
Distance → assigns ordinary nodes to CHs
ANN2 → selects Main CHs
```

Therefore, **ordinary-node cluster membership is currently distance-based, not directly ANN-based**.

This distinction is important when describing the project in a report or research paper.

---

# 📊 Unequal Cluster Sizes

Cluster sizes are not forced to be equal.

Example:

```text
CH 1 → 8 nodes
CH 2 → 15 nodes
CH 3 → 5 nodes
CH 4 → 11 nodes
```

The unequal distribution occurs naturally because ordinary nodes are assigned according to their nearest Cluster Head (CH).

---

# 📏 Cluster Size Calculation

```matlab
clusterSize = zeros(numberOfCH,1);

for k = 1:aliveNodes
    i = alive(k);
    clusterID = clusterAssignment(i);

    clusterSize(clusterID) = ...
        clusterSize(clusterID) + 1;
end
```

`clusterSize(j)` represents the number of nodes assigned to Cluster Head (CH) `j`.

---

# ⚡ Average Cluster Energy

After clusters are created, the actual average residual energy of each cluster is calculated.

```matlab
avgClusterEnergy = zeros(numberOfCH,1);

for j = 1:numberOfCH

    clusterNodes = ...
        find(clusterAssignment == j & [node.energy]' > 0);

    if isempty(clusterNodes)

        avgClusterEnergy(j) = 0;

    else

        clusterEnergy = ...
            [node(clusterNodes).energy];

        avgClusterEnergy(j) = ...
            mean(clusterEnergy);

    end
end
```

Every alive node in that cluster then receives the cluster's average energy value.

---

# 📦 Updating Cluster Head Information

Once cluster membership is known:

```matlab
for i = 1:SN

    clusterID = clusterAssignment(i);

    chNode = CH_Index(clusterID);

    node(i).CH_x = node(chNode).x;
    node(i).CH_y = node(chNode).y;
    node(i).CH_z = node(chNode).z;

end
```

The complete nine-feature `NodeInfo_Packet` can then be rebuilt.

---

# 🧠 Artificial Neural Network 2 (ANN2)

ANN2 is responsible for **Main Cluster Head (Main CH) selection**.

ANN2 operates only on selected Cluster Heads (CHs).

---

# 📊 ANN2 Inputs

ANN2 uses six features:

| Input | Feature |
|---|---|
| 1 | CH X coordinate |
| 2 | CH Y coordinate |
| 3 | CH Z coordinate |
| 4 | CH residual energy |
| 5 | CH distance to BS |
| 6 | Cluster size |

MATLAB:

```matlab
ANN2_Input = zeros(numberOfCH,6);

for j = 1:numberOfCH

    chNode = CH_Index(j);

    ANN2_Input(j,1) = node(chNode).x;
    ANN2_Input(j,2) = node(chNode).y;
    ANN2_Input(j,3) = node(chNode).z;
    ANN2_Input(j,4) = node(chNode).energy;
    ANN2_Input(j,5) = node(chNode).distanceBS;
    ANN2_Input(j,6) = clusterSize(j);

end
```

---

# 📊 ANN2 Normalization

ANN2 also uses min-max normalization:

```matlab
input2Min = min(ANN2_Input);
input2Max = max(ANN2_Input);
input2Range = input2Max - input2Min;

ANN2_Input_Norm = zeros(size(ANN2_Input));

for j = 1:6

    if input2Range(j) == 0

        ANN2_Input_Norm(:,j) = 0.5;

    else

        ANN2_Input_Norm(:,j) = ...
            (ANN2_Input(:,j) - input2Min(j)) ...
            / input2Range(j);

    end

end
```

---

# 🎯 ANN2 Prototype Target

The prototype uses:

```matlab
energyScore = ANN2_Input_Norm(:,4);
distanceScore = 1 - ANN2_Input_Norm(:,5);
clusterSizeScore = 1 - ANN2_Input_Norm(:,6);
```

The target is:

```matlab
ANN2_Target = ...
    0.4 * energyScore + ...
    0.3 * distanceScore + ...
    0.3 * clusterSizeScore;
```

Interpretation:

```text
Higher residual energy
        ↓
Higher suitability

Smaller BS distance
        ↓
Higher suitability

Smaller cluster size
        ↓
Higher suitability
```

Again, these weights are prototype design choices.

---

# 🏗️ ANN2 Architecture

```matlab
hiddenNeurons2 = 10;
net2 = feedforwardnet(hiddenNeurons2);
```

Conceptually:

```text
6 CH-level Inputs
       │
       ▼
10 Hidden Neurons
       │
       ▼
1 Main CH Suitability Score
```

Training:

```matlab
ANN2_Input_Train = ANN2_Input_Norm';
ANN2_Target_Train = ANN2_Target';

net2 = train( ...
    net2, ...
    ANN2_Input_Train, ...
    ANN2_Target_Train);
```

Prediction:

```matlab
ANN2_Output = net2(ANN2_Input_Train)';
```

---

# 👑 Main Cluster Head Selection

The Main Cluster Head (Main CH) growth factor is:

```matlab
q = 0.1;
```

The number of Main Cluster Heads is:

```matlab
numberOfMainCH = floor(q * numberOfCH);
numberOfMainCH = max(1,numberOfMainCH);
```

### Example

If:

```text
12 Cluster Heads
q = 0.1
```

then:

```text
0.1 × 12 = 1.2
floor(1.2) = 1
```

Therefore:

```text
1 Main Cluster Head
```

---

# 🏆 Main CH Selection

ANN2 outputs are sorted:

```matlab
[sortedMainScores, sortedMainIndex] = ...
    sort(ANN2_Output,'descend');
```

The top Cluster Head (CH) nodes are selected as Main Cluster Heads:

```matlab
MainCH_Index = ...
    CH_Index(sortedMainIndex(1:numberOfMainCH));
```

The hierarchy is:

```text
All Alive Nodes
      │
      ▼
     ANN1
      │
      ▼
     CHs
      │
      ▼
     ANN2
      │
      ▼
   Main CHs
```

---

# 📡 Time Division Multiple Access (TDMA)

**Time Division Multiple Access (TDMA)** is used as the logical scheduling mechanism for intra-cluster communication.

The concept is:

```text
Node A → Slot 1
Node B → Slot 2
Node C → Slot 3
Node D → Slot 4
```

This provides separate transmission opportunities to nodes belonging to the same cluster.

---

# 🕐 TDMA Slot Assignment

```matlab
TDMA_Slot = zeros(SN,1);

for j = 1:numberOfCH

    clusterNodes = ...
        find(clusterAssignment == j);

    for slot = 1:length(clusterNodes)

        nodeID = clusterNodes(slot);

        TDMA_Slot(nodeID) = slot;

    end

end
```

The current implementation represents TDMA scheduling logically.

It does not model a complete physical Medium Access Control (MAC) layer.

---

# 📡 Communication Architecture

The complete communication path is:

```text
Sensor Node
     │
     │ TDMA
     ▼
Cluster Head (CH)
     │
     │ Scheduled hierarchical communication
     ▼
Main Cluster Head (Main CH)
     │
     │ Long-range transmission
     ▼
Base Station (BS)
```

---

# 📡 Stage 1: Sensor Node → CH

Every alive non-Cluster-Head sensor node sends information to its assigned Cluster Head (CH).

The 3D distance is calculated.

The transmitting sensor node pays transmission energy.

The receiving Cluster Head (CH) pays reception energy.

---

# 📡 Stage 2: CH → Main CH

Every non-Main Cluster Head (CH) sends information to its nearest Main Cluster Head (Main CH).

The Cluster Head (CH) pays transmission energy.

The Main Cluster Head (Main CH) pays reception energy.

---

# 📡 Stage 3: Main CH → BS

Each Main Cluster Head (Main CH) sends its information toward the Base Station (BS).

This is the final communication stage.

---

# ⚡ Energy Model

The current prototype uses:

```matlab
packetLength = 4000;

ETX = 50e-9;
ERX = 50e-9;

Efs = 10e-12;

EDA = 5e-9;
```

| Parameter | Meaning | Default |
|---|---|---:|
| `packetLength` | Packet size | 4000 bits |
| `ETX` | Transmission electronics energy | 50e-9 J/bit |
| `ERX` | Reception electronics energy | 50e-9 J/bit |
| `Efs` | Free-space amplifier coefficient | 10e-12 J/bit/m² |
| `EDA` | Data aggregation energy | 5e-9 J/bit |

---

# 📐 Transmission Energy

The current prototype uses:

```matlab
txEnergy = packetLength * ETX + ...
           packetLength * Efs * distance^2;
```

Mathematically:

```text
E_TX = L × E_TX(electronics)
       + L × E_fs × d²
```

where:

- `L` = packet length.
- `d` = communication distance.

---

# 📥 Reception Energy

```matlab
rxEnergy = packetLength * ERX;
```

Mathematically:

```text
E_RX = L × E_RX(electronics)
```

---

# 🔄 Data Aggregation Energy

```matlab
aggregationEnergy = packetLength * EDA;
```

The current prototype applies aggregation energy at the Main Cluster Head (Main CH) based on the currently modeled received Cluster Head (CH) packets.

---

# ⚠️ Energy Model Limitation

The current model uses a free-space:

```text
d²
```

amplifier term.

A more advanced radio model can use different path-loss behavior for longer distances.

Before using the simulation for final research claims, the exact radio-energy model should be explicitly documented and validated against the intended reference methodology.

---

# 🔋 Energy Update

The simulation subtracts energy from the nodes participating in communication.

The general sequence is:

```text
Sensor transmission energy
        ↓
CH reception energy
        ↓
CH transmission energy
        ↓
Main CH reception energy
        ↓
Main CH aggregation energy
        ↓
Main CH transmission energy
```

Afterward:

```matlab
if node(i).energy < 0
    node(i).energy = 0;
end
```

---

# 💀 Alive and Dead Nodes

A node is considered alive when:

```matlab
node(i).energy > 0
```

A node is considered dead when:

```matlab
node(i).energy <= 0
```

At the beginning of each round:

```matlab
alive = find([node.energy] > 0);

aliveNodes = length(alive);

deadNodes = SN - aliveNodes;
```

---

# 🔁 Dynamic Round Operation

The simulation uses:

```matlab
while true
```

instead of fixing a maximum number of rounds.

The loop stops when:

```matlab
aliveNodes == 0
```

This allows the simulation to determine the actual lifetime produced by the selected network parameters.

---

# 🔄 Complete Per-Round Algorithm

Each round follows:

```text
1. Find alive nodes
2. Update distance to BS
3. Construct ANN1 input
4. Normalize ANN1 input
5. Run ANN1
6. Select CHs
7. Form clusters
8. Calculate cluster sizes
9. Calculate average cluster energy
10. Update CH coordinates
11. Construct ANN2 input
12. Normalize ANN2 input
13. Run ANN2
14. Select Main CHs
15. Assign TDMA slots
16. Sensor Node → CH communication
17. CH → Main CH communication
18. Main CH → BS communication
19. Calculate energy consumption
20. Update residual energy
21. Count alive/dead nodes
22. Save round information
23. Move to next round
```

---

# 👀 Monitoring Every Round

The simulation can print the exact Cluster Head (CH) and Main Cluster Head (Main CH) node IDs.

Example:

```text
========================================
ROUND 1
========================================
Alive Nodes   = 100
Dead Nodes    = 0
Number of CHs = 10
CH Node IDs: 5 12 19 27 34 46 51 63 79 91

Number of Main CHs = 1
Main CH Node IDs: 46
========================================
```

This makes it possible to see exactly which node was selected in every round.

---

# 🗃️ Saving CH Selection History

Before the simulation loop:

```matlab
CH_History = cell(0,1);
MainCH_History = cell(0,1);
```

After CH selection:

```matlab
CH_History{round} = CH_Index;
```

After Main CH selection:

```matlab
MainCH_History{round} = MainCH_Index;
```

Then:

```matlab
CH_History{1}
```

shows Round 1 CHs.

```matlab
CH_History{2}
```

shows Round 2 CHs.

Similarly:

```matlab
MainCH_History{1}
MainCH_History{2}
```

show the Main CH selections.

---

# 📊 Why Selection History Matters

The selection history can be used to analyze:

- CH rotation.
- Main CH rotation.
- Number of times each node becomes CH.
- Number of times each node becomes Main CH.
- Whether particular nodes are repeatedly selected.
- Whether low-energy nodes are repeatedly selected.
- How role selection changes as the network ages.

---

# 🧠 Current-State-Based Selection

The current architecture does not use a permanent:

```text
CH = 1
Normal = 0
```

label for ANN1 training.

Instead, ANN1 uses current node information.

A node can therefore change roles between rounds.

This is important because a node's energy and network position change over time.

---

# 📊 Network Lifetime Metrics

The simulation records:

```matlab
roundNumber
aliveNodeCount
deadNodeCount
totalEnergy
```

These arrays are used for lifetime analysis.

---

# 💀 First Node Death

The First Node Death (FND) round is the first round in which at least one node has died.

```matlab
firstDeadIndex = ...
    find(deadNodeCount >= 1,1);
```

Then:

```matlab
firstNodeDeathRound = ...
    roundNumber(firstDeadIndex);
```

---

# 💀 Half Node Death

The half-node-death metric is defined here as the first round in which at least half of the original sensor nodes are dead.

```matlab
halfDeadIndex = ...
    find(deadNodeCount >= floor(SN/2),1);
```

Then:

```matlab
halfNodeDeathRound = ...
    roundNumber(halfDeadIndex);
```

---

# 💀 Last Node Death

The Last Node Death occurs when:

```matlab
aliveNodeCount == 0
```

The corresponding round is stored as:

```matlab
lastNodeDeathRound
```

---

# 📈 Total Simulation Rounds

The total recorded rounds are:

```matlab
roundNumber(end)
```

The simulation does not assume beforehand that the lifetime will be:

```text
1000
1500
2000
```

or another fixed number.

The actual number of rounds is determined by energy depletion.

---

# 📊 Visualization

The project uses three main visualization categories.

## 1. Initial 3D Deployment

Shows:

- Sensor nodes.
- Node IDs.
- Base Station (BS).
- X axis.
- Y axis.
- Z axis.

---

## 2. Alive/Dead Node Plot

Shows:

```text
Round vs Number of Nodes
```

with:

- Alive Nodes.
- Dead Nodes.

---

## 3. Total Network Energy

Shows:

```text
Round vs Total Residual Energy
```

---

## 4. Final 3D Network

Shows:

```text
Alive Nodes
Dead Nodes
Cluster Heads
Main Cluster Heads
Base Station
```

---

# 🖥️ Visualization Legend

The current visualization uses:

| Display | Meaning |
|---|---|
| Blue | Alive sensor nodes |
| Black | Dead sensor nodes |
| Green | Cluster Heads (CHs) |
| Magenta | Main Cluster Heads (Main CHs) |
| Red | Base Station (BS) |

These colors are only visualization choices.

---

# 📊 Final 3D Plot Important Note

The final 3D plot represents the role state stored at the end of the simulation.

It does **not** show every CH selected throughout the entire simulation.

For historical selection information, use:

```matlab
CH_History
MainCH_History
```

---

# 📋 Default Parameters

| Parameter | MATLAB Variable | Default |
|---|---|---:|
| Sensor nodes | `SN` | 100 |
| X dimension | `area_x` | 100 m |
| Y dimension | `area_y` | 100 m |
| Z dimension | `area_z` | 100 m |
| Initial energy | `Eo` | 0.5 J |
| CH growth factor | `p` | 0.1 |
| Main CH growth factor | `q` | 0.1 |
| Packet length | `packetLength` | 4000 bits |
| Transmission electronics | `ETX` | 50e-9 J/bit |
| Reception electronics | `ERX` | 50e-9 J/bit |
| Free-space coefficient | `Efs` | 10e-12 J/bit/m² |
| Aggregation energy | `EDA` | 5e-9 J/bit |
| ANN1 hidden neurons | `hiddenNeurons` | 10 |
| ANN2 hidden neurons | `hiddenNeurons2` | 10 |

---

# 📚 Variable Reference

| Variable | Meaning |
|---|---|
| `SN` | Total number of sensor nodes |
| `area_x` | X dimension |
| `area_y` | Y dimension |
| `area_z` | Z dimension |
| `Eo` | Initial node energy |
| `BS` | Base Station structure |
| `node` | Sensor node structure array |
| `NodeInfo_Packet` | Nine-feature node information matrix |
| `X` | Node information matrix reference |
| `ANN1_Input` | ANN1 input |
| `ANN1_Target` | ANN1 prototype target |
| `ANN1_Output` | ANN1 suitability score |
| `net1` | ANN1 model |
| `p` | CH growth factor |
| `CH_Index` | Selected CH node IDs |
| `clusterAssignment` | Cluster assignment of nodes |
| `clusterSize` | Size of each cluster |
| `avgClusterEnergy` | Average energy of each cluster |
| `ANN2_Input` | ANN2 input |
| `ANN2_Target` | ANN2 prototype target |
| `ANN2_Output` | ANN2 suitability score |
| `net2` | ANN2 model |
| `q` | Main CH growth factor |
| `MainCH_Index` | Selected Main CH IDs |
| `TDMA_Slot` | TDMA slot of each node |
| `packetLength` | Packet size |
| `ETX` | Transmission electronics energy |
| `ERX` | Reception electronics energy |
| `Efs` | Free-space amplifier coefficient |
| `EDA` | Data aggregation energy |
| `energyConsumed` | Sensor transmission energy |
| `CH_ReceiveEnergy` | CH reception energy |
| `CH_TransmitEnergy` | CH transmission energy |
| `MainCH_ReceiveEnergy` | Main CH reception energy |
| `MainCH_AggregationEnergy` | Main CH aggregation energy |
| `MainCH_TransmitEnergy` | Main CH transmission energy |
| `roundNumber` | Simulation round history |
| `aliveNodeCount` | Alive nodes per round |
| `deadNodeCount` | Dead nodes per round |
| `totalEnergy` | Total residual network energy |
| `CH_History` | CH selection history |
| `MainCH_History` | Main CH selection history |

---

# 🧮 Algorithm Pseudocode

```text
INITIALIZE

Set SN
Set network dimensions
Set initial energy
Set Base Station position

Deploy SN nodes randomly in 3D

For every node:
    Store X, Y, Z
    Store initial energy
    Calculate distance to BS

Calculate initial average energy

Create NodeInfo_Packet

Prepare ANN1
Train ANN1

Prepare ANN2
Train ANN2

Initialize history arrays

START ROUND LOOP

While at least one node is alive:

    Find alive nodes

    Update node-to-BS distances

    Create ANN1 input

    Normalize ANN1 input

    Predict ANN1 scores

    Calculate CH count:
        floor(p × alive nodes)

    Select top ANN1 nodes as CHs

    Form clusters using nearest CH

    Calculate cluster sizes

    Calculate average cluster energy

    Update CH coordinates

    Create ANN2 input

    Normalize ANN2 input

    Predict ANN2 scores

    Calculate Main CH count:
        floor(q × CH count)

    Select top ANN2 CHs as Main CHs

    Save CH history

    Save Main CH history

    Assign TDMA slots

    Perform Sensor Node → CH communication

    Calculate CH reception energy

    Perform CH → Main CH communication

    Calculate Main CH reception energy

    Perform Main CH → BS communication

    Calculate aggregation energy

    Update node energy

    Set negative energy to zero

    Count alive nodes

    Count dead nodes

    Store round results

    Increment round

END LOOP

Calculate FND

Calculate Half Node Death

Calculate Last Node Death

Generate result plots

Generate final 3D network plot

END
```

---

# 🧪 MATLAB Implementation

## Initial Environment

```matlab
clear;
clc;
close all;
```

---

## Basic Network Setup

```matlab
SN = 100;

area_x = 100;
area_y = 100;
area_z = 100;

Eo = 0.5;

BS.x = 50;
BS.y = 50;
BS.z = 0;
```

---

## Random 3D Deployment

```matlab
for i = 1:SN

    node(i).x = rand * area_x;
    node(i).y = rand * area_y;
    node(i).z = rand * area_z;

    node(i).energy = Eo;

    node(i).distanceBS = sqrt( ...
        (node(i).x - BS.x)^2 + ...
        (node(i).y - BS.y)^2 + ...
        (node(i).z - BS.z)^2);

    node(i).avgClusterEnergy = 0;

    node(i).CH_x = 0;
    node(i).CH_y = 0;
    node(i).CH_z = 0;

end
```

---

# ▶️ How to Run

## 1. Open MATLAB

Open MATLAB and navigate to the project directory.

---

## 2. Check Required Neural Network Functions

Run:

```matlab
which feedforwardnet
which train
```

If MATLAB cannot find these functions, check the installed toolbox/functionality required by the MATLAB release.

---

## 3. Open the Main Script

Open the main MATLAB script containing:

```matlab
SN
area_x
area_y
area_z
Eo
BS
```

---

## 4. Run the Script

Run the complete script.

The program will:

```text
Deploy nodes
↓
Train ANN1
↓
Train ANN2
↓
Start rounds
↓
Select CHs
↓
Select Main CHs
↓
Communicate
↓
Consume energy
↓
Repeat
↓
All nodes die
↓
Display results
```

---

# 🔍 Debugging

When debugging, inspect the simulation in this order:

```text
1. Node coordinates
2. Node energy
3. Alive node list
4. ANN1 input
5. ANN1 output
6. CH_Index
7. Cluster assignment
8. Cluster size
9. Average cluster energy
10. ANN2 input
11. ANN2 output
12. MainCH_Index
13. Communication distances
14. Energy consumption
15. Updated energy
16. Alive/dead count
```

---

# 🧪 Useful MATLAB Checks

Check Node Information Packet:

```matlab
size(NodeInfo_Packet)
```

Check ANN1:

```matlab
size(ANN1_Input)
size(ANN1_Output)
```

Check Cluster Heads:

```matlab
CH_Index
```

Check cluster sizes:

```matlab
clusterSize
```

Check ANN2:

```matlab
size(ANN2_Input)
size(ANN2_Output)
```

Check Main Cluster Heads:

```matlab
MainCH_Index
```

Check energy:

```matlab
[node.energy]
```

---

# ⚠️ Common MATLAB Problems

## Dimension mismatch

MATLAB Artificial Neural Network (ANN) functions generally use:

```text
features × samples
```

Therefore:

```matlab
ANN1_Input_Train = ANN1_Input_Norm';
```

rather than:

```matlab
ANN1_Input_Train = ANN1_Input_Norm;
```

The same principle applies to ANN2.

---

## Zero normalization range

If:

```matlab
inputRange(j) == 0
```

the implementation uses:

```matlab
0.5
```

to avoid division by zero.

---

## Zero Cluster Heads

When the number of alive nodes becomes small:

```matlab
floor(p * aliveNodes)
```

may become zero.

Therefore:

```matlab
numberOfCH = max(1,numberOfCH);
```

is used while nodes remain alive.

---

## Zero Main Cluster Heads

Similarly:

```matlab
numberOfMainCH = max(1,numberOfMainCH);
```

is used while Cluster Heads (CHs) exist.

---

# 🎲 Reproducibility

The deployment uses MATLAB's random number generator:

```matlab
rand
```

Therefore, every execution can generate a different topology.

This can change:

- Cluster Head (CH) selections.
- Main Cluster Head (Main CH) selections.
- Cluster sizes.
- Communication distances.
- Energy consumption.
- Network lifetime.

For reproducibility:

```matlab
rng(1);
```

can be placed before node deployment.

For research experiments, multiple independent random seeds should normally be used.

---

# 🧪 Experimental Methodology

A single simulation run should not be treated as sufficient evidence for a general performance claim.

A stronger experimental setup should use multiple independent runs.

Example:

```text
Run 1
Run 2
Run 3
...
Run N
```

For each run, record:

- First Node Death.
- Half Node Death.
- Last Node Death.
- Total rounds.
- Total residual energy.
- Number of alive nodes.
- Number of dead nodes.
- Communication energy.
- Other selected performance metrics.

Then calculate appropriate statistics.

---

# ⚖️ Baseline Comparison

For comparison against another protocol, use consistent:

```text
Sensor node count
Network dimensions
Base Station position
Initial energy
Packet size
Energy model
Random topology
Simulation termination condition
Number of independent runs
```

Where appropriate, the same random deployment can be used for each protocol.

This reduces the effect of topology differences on the comparison.

---

# 📊 Suggested Performance Metrics

The current prototype directly supports:

- First Node Death (FND).
- Half Node Death.
- Last Node Death.
- Total simulation rounds.
- Alive nodes per round.
- Dead nodes per round.
- Total residual energy.

Future metrics can include:

- Throughput.
- Packet Delivery Ratio (PDR).
- End-to-end delay.
- Control overhead.
- Energy efficiency.
- Average residual energy.
- Energy variance.
- CH selection frequency.

---

# 📦 Throughput

Throughput is not currently fully implemented.

A future definition could be:

```text
Throughput =
Successfully delivered bits / simulation time
```

Before implementation, define exactly what constitutes a successfully delivered packet.

For example:

```text
Sensor → CH
```

and:

```text
Sensor → CH → Main CH → BS
```

are different measurement points.

---

# 📡 Packet Delivery Ratio (PDR)

Packet Delivery Ratio (PDR) is not currently implemented.

A possible definition is:

```text
PDR =
Successfully delivered packets
--------------------------------
Transmitted packets
```

The exact measurement point must be defined before implementation.

---

# ⏱️ Delay

End-to-end delay is not currently implemented.

A future implementation could model:

```text
Sensor Node
    ↓
TDMA waiting time
    ↓
CH
    ↓
Main CH
    ↓
BS
```

and measure the total time required for data to reach the Base Station (BS).

---

# 📈 Energy Fairness

A future analysis can evaluate whether energy consumption is balanced.

Useful measurements include:

```text
Minimum residual energy
Maximum residual energy
Mean residual energy
Standard deviation of residual energy
Energy consumed per round
CH selections per node
Main CH selections per node
```

---

# 🧠 ANN Limitations

## ANN1

Current ANN1 learns a manually defined target:

```text
0.4 × Energy
+
0.3 × Distance
+
0.3 × Cluster Energy
```

Therefore, ANN1 is currently approximating a predefined scoring function.

It is not independently discovering an optimal policy.

---

## ANN2

ANN2 similarly approximates:

```text
0.4 × Energy
+
0.3 × Distance
+
0.3 × Cluster Size
```

The weights are prototype design choices.

---

# 🔄 ANN Training Limitation

The current design trains:

```text
ANN1 → once
ANN2 → once
```

and then uses them during every simulation round.

They are not retrained after every round.

This means the networks perform dynamic inference using current inputs, but their learned parameters are not continuously updated from newly generated round data.

---

# 📊 Training Data Limitation

The current prototype does not use a large external dataset.

Instead, the prototype targets are generated from manually specified formulas.

A future research version could use:

- Optimization-generated labels.
- Simulation-generated datasets.
- Real Wireless Sensor Network (WSN) measurements.
- Reinforcement learning.
- Multi-objective optimization.

---

# 🧩 Cluster Membership Limitation

Current architecture:

```text
ANN1 → CH selection
Nearest distance → cluster membership
ANN2 → Main CH selection
```

If future work requires ANN-based cluster membership, an additional node-to-CH suitability model can be introduced.

Possible factors:

```text
Distance
Residual energy
CH energy
Cluster load
Link quality
Expected transmission energy
```

---

# 📡 Link Quality

The current implementation does not explicitly use a measured link-quality feature.

Possible future features include:

```text
Received Signal Strength Indicator (RSSI)
Link Quality Indicator (LQI)
Packet Delivery Ratio (PDR)
Bit Error Rate (BER)
```

Any added feature must have:

1. A defined measurement method.
2. A consistent numerical representation.
3. Appropriate normalization.
4. Corresponding training data.

---

# ⚡ Energy Model Limitations

The current model does not fully simulate:

- Radio idle energy.
- Sleep energy.
- Control packet energy.
- Retransmissions.
- Packet collisions.
- Radio startup energy.
- Variable packet sizes.
- Physical-layer modulation.
- Real link failures.

These can be added in future versions.

---

# 📦 Aggregation Limitation

The current implementation models aggregation energy primarily for packets received by the Main Cluster Head (Main CH) from other Cluster Heads (CHs).

A more detailed packet-level model should explicitly define:

```text
How many packets each CH generates
How many packets are received
How aggregation changes packet size
How many packets are forwarded
```

---

# 🚀 Future Improvements

## Phase 1 — Simulation Correctness

- Verify every energy calculation.
- Verify cluster membership.
- Verify CH selection.
- Verify Main CH selection.
- Verify termination.
- Verify packet counts.

---

## Phase 2 — Detailed Logging

Add history for:

```text
CH IDs
Main CH IDs
ANN1 scores
ANN2 scores
Cluster sizes
Communication distances
Energy consumed per node
```

---

## Phase 3 — Additional Metrics

Add:

```text
Throughput
Packet Delivery Ratio
Delay
Control overhead
Energy efficiency
```

---

## Phase 4 — Advanced ANN Training

Investigate:

```text
Optimization-generated labels
Reinforcement learning
Online learning
Historical simulation datasets
Multi-objective learning
```

---

## Phase 5 — Advanced Routing

Investigate:

```text
Multi-hop CH routing
Link-quality-aware routing
Adaptive Main CH count
Load balancing
Distance-aware routing
Energy-aware routing
```

---

## Phase 6 — Statistical Validation

Perform:

```text
Multiple independent simulations
Mean calculation
Standard deviation
Confidence intervals
Appropriate statistical hypothesis tests
```

---

# 🔬 Research Notes

## Current Decision Hierarchy

The most important architectural distinction is:

```text
ANN1
  ↓
Select CHs

Distance
  ↓
Assign ordinary nodes to CHs

ANN2
  ↓
Select Main CHs
```

This should remain explicit when describing the current implementation.

---

## CH Growth Factor

```matlab
p = 0.1;
```

Number of CHs:

```matlab
floor(p * aliveNodes)
```

---

## Main CH Growth Factor

```matlab
q = 0.1;
```

Number of Main CHs:

```matlab
floor(q * numberOfCH)
```

---

## Example

For:

```text
100 alive nodes
```

CH count:

```text
floor(0.1 × 100) = 10
```

Then:

```text
10 CHs
```

Main CH count:

```text
floor(0.1 × 10) = 1
```

Therefore:

```text
100 alive nodes
→ 10 CHs
→ 1 Main CH
→ BS
```

For:

```text
37 alive nodes
```

CH count:

```text
floor(0.1 × 37) = 3
```

Main CH count:

```text
floor(0.1 × 3) = 0
```

The safety rule changes this to:

```text
1 Main CH
```

while CHs exist.

---

# 📦 Feature Summary

## Complete Node Information Packet

```text
[X,
 Y,
 Z,
 Energy,
 Distance-to-BS,
 Average-Cluster-Energy,
 CH-X,
 CH-Y,
 CH-Z]
```

Total:

```text
9 features
```

---

## ANN1

```text
[X,
 Y,
 Z,
 Energy,
 Distance-to-BS,
 Average-Cluster-Energy]
```

Total:

```text
6 inputs
```

Output:

```text
CH suitability score
```

---

## ANN2

```text
[CH-X,
 CH-Y,
 CH-Z,
 CH-Energy,
 CH-Distance-to-BS,
 Cluster-Size]
```

Total:

```text
6 inputs
```

Output:

```text
Main CH suitability score
```

---

# 🔄 Complete Communication Path

```text
                 ┌──────────────────┐
                 │  Sensor Node 1   │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │  Sensor Node 2   │
                 └────────┬─────────┘
                          │
                     TDMA / local
                          │
                          ▼
                 ┌──────────────────┐
                 │  Cluster Head    │
                 │      (CH)        │
                 └────────┬─────────┘
                          │
                          │
                          ▼
                 ┌──────────────────┐
                 │    Main CH       │
                 │                  │
                 └────────┬─────────┘
                          │
                          │
                          ▼
                 ┌──────────────────┐
                 │  Base Station    │
                 │      (BS)        │
                 └──────────────────┘
```

---

# 🗺️ Project Architecture at a Glance

```text
                 3D Wireless Sensor Network
                            │
                            ▼
                  Current Node Information
                            │
                            ▼
                   ┌─────────────────┐
                   │      ANN1       │
                   │ Node Evaluation │
                   └────────┬────────┘
                            │
                            ▼
                    Cluster Heads
                         (CHs)
                            │
                            ▼
                 3D Distance Clustering
                            │
                            ▼
                Cluster Size + Energy
                            │
                            ▼
                   ┌─────────────────┐
                   │      ANN2       │
                   │ CH Evaluation   │
                   └────────┬────────┘
                            │
                            ▼
                   Main Cluster Head
                       (Main CH)
                            │
                            ▼
                     TDMA / Routing
                            │
                            ▼
                     Base Station
                         (BS)
                            │
                            ▼
                   Energy Consumption
                            │
                            ▼
                      Next Round
```

---

# 📊 Network Lifetime Output

The final simulation should report:

```text
========================================
        NETWORK LIFETIME RESULTS
========================================
First Node Death Round  = ...
Half Node Death Round   = ...
Last Node Death Round   = ...
Total Simulation Rounds = ...
========================================
```

The values are produced from the actual simulation and should not be manually specified.

---

# 🧪 Reproducibility Checklist

Before reporting experimental results, record:

```text
[ ] MATLAB version
[ ] Required toolbox/functionality
[ ] SN
[ ] Network X dimension
[ ] Network Y dimension
[ ] Network Z dimension
[ ] Base Station position
[ ] Initial energy
[ ] Packet length
[ ] ETX
[ ] ERX
[ ] Efs
[ ] EDA
[ ] p
[ ] q
[ ] ANN1 architecture
[ ] ANN2 architecture
[ ] ANN1 target weights
[ ] ANN2 target weights
[ ] Random seed
[ ] Number of independent runs
[ ] Termination condition
[ ] Baseline parameters
```

---

# 📁 Suggested GitHub Repository Structure

A clean repository can be organized as:

```text
ANN-3D-WSN/
│
├── README.md
│
├── MATLAB/
│   ├── main.m
│   ├── deployment.m
│   ├── ANN1.m
│   ├── ANN2.m
│   ├── clustering.m
│   ├── communication.m
│   ├── energy_model.m
│   └── plotting.m
│
├── Results/
│   ├── figures/
│   ├── tables/
│   └── simulation_results/
│
├── Documentation/
│   ├── architecture.md
│   └── methodology.md
│
├── References/
│   └── papers/
│
└── LICENSE
```

If the implementation is currently contained in one MATLAB file, it is also acceptable to begin with:

```text
ANN-3D-WSN/
│
├── README.md
├── main.m
├── Results/
└── References/
```

and split the MATLAB implementation into separate functions later.

---

# 📚 References

The project is inspired by research concerning:

- Low-Energy Adaptive Clustering Hierarchy (LEACH).
- Artificial Neural Network (ANN)-assisted Wireless Sensor Network (WSN) clustering.
- Energy-aware clustering.
- Hierarchical routing.
- Wireless Sensor Network lifetime optimization.

Reference papers used during project development should be added to the repository's `References/` directory and cited explicitly in the final research documentation.

Example:

```text
References/
├── LEACH_reference.pdf
├── ANN_LEACH_reference.pdf
└── additional_reference.pdf
```

> **Note:** The prototype's ANN target weights and some implementation details are design choices and should not be attributed to a reference paper unless the corresponding source explicitly defines them.

---

# 📝 Terminology

| Short Form | Full Form |
|---|---|
| WSN | Wireless Sensor Network |
| ANN | Artificial Neural Network |
| ANN1 | First Artificial Neural Network |
| ANN2 | Second Artificial Neural Network |
| LEACH | Low-Energy Adaptive Clustering Hierarchy |
| CH | Cluster Head |
| Main CH | Main Cluster Head |
| BS | Base Station |
| TDMA | Time Division Multiple Access |
| RSSI | Received Signal Strength Indicator |
| LQI | Link Quality Indicator |
| PDR | Packet Delivery Ratio |
| FND | First Node Death |
| BER | Bit Error Rate |

---

# ⚠️ Important Terminology Rule

The upper-level Cluster Head must be referred to as:

> **Main Cluster Head (Main CH)**

throughout the project.

---

# 📌 Final Summary

The current project implements a two-stage intelligent hierarchy for a 3D Wireless Sensor Network:

```text
3D Sensor Deployment
        ↓
Current Node State
        ↓
Artificial Neural Network 1
        ↓
Cluster Head Selection
        ↓
3D Nearest-CH Cluster Formation
        ↓
Cluster Size + Average Cluster Energy
        ↓
Artificial Neural Network 2
        ↓
Main Cluster Head Selection
        ↓
TDMA-Based Communication
        ↓
Sensor Node → CH
        ↓
CH → Main CH
        ↓
Main CH → BS
        ↓
Energy Update
        ↓
Lifetime Measurement
        ↓
Next Round
```

The central idea is **dynamic current-state-based selection**.

The first Artificial Neural Network (ANN1) evaluates sensor nodes for Cluster Head (CH) selection.

The second Artificial Neural Network (ANN2) evaluates selected Cluster Heads (CHs) for Main Cluster Head (Main CH) selection.

The number of Cluster Heads (CHs) is controlled using:

```text
p = 0.1
```

and the number of Main Cluster Heads (Main CHs) is controlled using:

```text
q = 0.1
```

Both use the `floor` operation.

The simulation continues dynamically until all sensor nodes have exhausted their modeled energy.

---

# 🚀 Future Research Direction

The current implementation provides a foundation for progressively adding:

```text
          Current Prototype
                 │
                 ▼
       ┌──────────────────┐
       │ Better ANN Data  │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Link Quality     │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ ANN-Based        │
       │ Membership       │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Multi-Hop Routing│
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Throughput / PDR │
       │ / Delay          │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Statistical      │
       │ Validation       │
       └──────────────────┘
```

The final research version should clearly distinguish between:

- Literature-derived methodology.
- Prototype design decisions.
- Simulation assumptions.
- Measured results.
- Future extensions.

---

## 📄 License

Add the project's chosen license here.

For example:

```text
MIT License
```

or another license appropriate for the repository.

---

## 👨‍💻 Project

**Artificial Neural Network-Assisted 3D Wireless Sensor Network**

**Primary environment:** MATLAB

**Core concepts:**

```text
Wireless Sensor Network
Artificial Neural Network
LEACH
3D Clustering
Cluster Head Selection
Main Cluster Head Selection
TDMA
Energy-Aware Routing
Network Lifetime
```
