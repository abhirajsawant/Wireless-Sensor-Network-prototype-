# ============================================================
# 1_08 - COMMUNICATION MODEL
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import numpy as np
import pandas as pd
import importlib.util
from pathlib import Path


# ============================================================
# 1_08_01 - LOAD CONFIGURATION
# ============================================================

CURRENT_FOLDER = Path(__file__).resolve().parent


def load_module(module_name, file_name):

    file_path = CURRENT_FOLDER / file_name

    spec = importlib.util.spec_from_file_location(
        module_name,
        file_path
    )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module


config = load_module(
    "config",
    "1_01_config.py"
)

energy_model = load_module(
    "energy_model",
    "1_07_energy.py"
)

deployment = load_module(
    "deployment",
    "1_02_deployment.py"
)

ann1 = load_module(
    "ann1",
    "1_04_ANN1_CH_Selection.py"
)

clustering = load_module(
    "clustering",
    "1_05_clustering.py"
)

ann2 = load_module(
    "ann2",
    "1_06_ANN2_Main_CH.py"
)


# ============================================================
# 1_08_02 - DISTANCE CALCULATION
# ============================================================

def calculate_distance(node_a, node_b):

    dx = float(node_a["x"]) - float(node_b["x"])
    dy = float(node_a["y"]) - float(node_b["y"])
    dz = float(node_a["z"]) - float(node_b["z"])

    distance = np.sqrt(
        dx**2 +
        dy**2 +
        dz**2
    )

    return distance


# ============================================================
# 1_08_03 - TDMA SLOT ASSIGNMENT
# ============================================================

def assign_tdma_slots(nodes):

    nodes = nodes.copy()

    nodes["TDMA_Slot"] = -1

    cluster_ids = sorted(
        nodes.loc[
            nodes["ClusterID"] >= 0,
            "ClusterID"
        ].unique()
    )

    for cluster_id in cluster_ids:

        cluster_members = nodes[
            nodes["ClusterID"] == cluster_id
        ].index.tolist()

        slot_number = 1

        for node_index in cluster_members:

            # The CH itself does not need a normal
            # member transmission slot.
            if nodes.loc[node_index, "Is_CH"]:

                nodes.loc[
                    node_index,
                    "TDMA_Slot"
                ] = 0

            else:

                nodes.loc[
                    node_index,
                    "TDMA_Slot"
                ] = slot_number

                slot_number += 1

    return nodes


# ============================================================
# 1_08_04 - MEMBER NODE -> CLUSTER HEAD
# ============================================================

def member_to_cluster_head(nodes):

    nodes = nodes.copy()

    communication_records = []

    for node_index, node in nodes.iterrows():

        # Skip dead nodes
        if node["energy"] <= 0:
            continue

        # Skip CH nodes
        if bool(node["Is_CH"]):
            continue

        ch_id = int(node["CH_ID"])

        ch_rows = nodes[
            nodes["NodeID"] == ch_id
        ]

        if ch_rows.empty:
            continue

        ch = ch_rows.iloc[0]

        distance = calculate_distance(
            node,
            ch
        )

        tx_energy = energy_model.transmission_energy(
            energy_model.PACKET_SIZE,
            distance
        )

        old_energy = float(
            nodes.loc[node_index, "energy"]
        )

        new_energy = energy_model.consume_energy(
            old_energy,
            tx_energy
        )

        nodes.loc[
            node_index,
            "energy"
        ] = new_energy

        communication_records.append({

            "Sender": int(node["NodeID"]),

            "Receiver": int(ch["NodeID"]),

            "Link": "Node_to_CH",

            "Distance": distance,

            "EnergyConsumed": tx_energy,

            "TDMA_Slot": int(
                node["TDMA_Slot"]
            )

        })

    nodes = energy_model.update_alive_status(
        nodes
    )

    return nodes, communication_records


# ============================================================
# 1_08_05 - CH RECEIVE + AGGREGATE
# ============================================================

def cluster_head_receive_and_aggregate(
    nodes
):

    nodes = nodes.copy()

    communication_records = []

    ch_indices = nodes.index[
        nodes["Is_CH"] == True
    ].tolist()

    for ch_index in ch_indices:

        ch = nodes.loc[ch_index]

        if ch["energy"] <= 0:
            continue

        cluster_id = int(
            ch["ClusterID"]
        )

        members = nodes[
            (nodes["ClusterID"] == cluster_id) &
            (nodes["NodeID"] != ch["NodeID"])
        ]

        alive_members = members[
            members["energy"] > 0
        ]

        number_of_packets = len(
            alive_members
        )

        if number_of_packets == 0:
            continue

        receive_aggregation_energy = (
            energy_model.ch_receive_aggregation_energy(
                number_of_packets,
                energy_model.PACKET_SIZE
            )
        )

        old_energy = float(
            nodes.loc[ch_index, "energy"]
        )

        new_energy = energy_model.consume_energy(
            old_energy,
            receive_aggregation_energy
        )

        nodes.loc[
            ch_index,
            "energy"
        ] = new_energy

        communication_records.append({

            "Sender": "Cluster Members",

            "Receiver": int(
                ch["NodeID"]
            ),

            "Link": "CH_RX_Aggregation",

            "Distance": 0.0,

            "PacketsReceived":
                number_of_packets,

            "EnergyConsumed":
                receive_aggregation_energy

        })

    nodes = energy_model.update_alive_status(
        nodes
    )

    return nodes, communication_records


# ============================================================
# 1_08_06 - CH -> MAIN CH
# ============================================================

def cluster_head_to_main_ch(
    nodes,
    main_ch_id
):

    nodes = nodes.copy()

    communication_records = []

    main_ch_rows = nodes[
        nodes["NodeID"] == main_ch_id
    ]

    if main_ch_rows.empty:

        return nodes, communication_records

    main_ch = main_ch_rows.iloc[0]

    ch_indices = nodes.index[
        nodes["Is_CH"] == True
    ].tolist()

    for ch_index in ch_indices:

        ch = nodes.loc[ch_index]

        # Main CH does not transmit to itself
        if int(ch["NodeID"]) == int(main_ch_id):
            continue

        # Dead CH cannot transmit
        if ch["energy"] <= 0:
            continue

        distance = calculate_distance(
            ch,
            main_ch
        )

        tx_energy = energy_model.transmission_energy(
            energy_model.PACKET_SIZE,
            distance
        )

        old_energy = float(
            nodes.loc[ch_index, "energy"]
        )

        new_energy = energy_model.consume_energy(
            old_energy,
            tx_energy
        )

        nodes.loc[
            ch_index,
            "energy"
        ] = new_energy

        communication_records.append({

            "Sender": int(
                ch["NodeID"]
            ),

            "Receiver": int(
                main_ch_id
            ),

            "Link": "CH_to_Main_CH",

            "Distance": distance,

            "EnergyConsumed": tx_energy

        })

    nodes = energy_model.update_alive_status(
        nodes
    )

    return nodes, communication_records


# ============================================================
# 1_08_07 - MAIN CH -> BASE STATION
# ============================================================

def main_ch_to_base_station(
    nodes,
    base_station,
    main_ch_id
):

    nodes = nodes.copy()

    communication_records = []

    main_ch_rows = nodes[
        nodes["NodeID"] == main_ch_id
    ]

    if main_ch_rows.empty:

        return nodes, communication_records

    main_ch_index = main_ch_rows.index[0]

    main_ch = nodes.loc[
        main_ch_index
    ]

    if main_ch["energy"] <= 0:

        return nodes, communication_records

    distance = calculate_distance(
        main_ch,
        base_station
    )

    tx_energy = energy_model.transmission_energy(
        energy_model.PACKET_SIZE,
        distance
    )

    old_energy = float(
        nodes.loc[
            main_ch_index,
            "energy"
        ]
    )

    new_energy = energy_model.consume_energy(
        old_energy,
        tx_energy
    )

    nodes.loc[
        main_ch_index,
        "energy"
    ] = new_energy

    communication_records.append({

        "Sender": int(main_ch_id),

        "Receiver": "Base Station",

        "Link": "Main_CH_to_BS",

        "Distance": distance,

        "EnergyConsumed": tx_energy

    })

    nodes = energy_model.update_alive_status(
        nodes
    )

    return nodes, communication_records


# ============================================================
# 1_08_08 - COMPLETE COMMUNICATION ROUND
# ============================================================

def run_communication_round(
    nodes,
    base_station,
    main_ch_id
):

    nodes = nodes.copy()

    # --------------------------------------------------------
    # Step 1 - Assign TDMA slots
    # --------------------------------------------------------

    nodes = assign_tdma_slots(
        nodes
    )

    all_records = []

    # --------------------------------------------------------
    # Step 2 - Sensor nodes -> CH
    # --------------------------------------------------------

    nodes, records = member_to_cluster_head(
        nodes
    )

    all_records.extend(records)

    # --------------------------------------------------------
    # Step 3 - CH receives and aggregates
    # --------------------------------------------------------

    nodes, records = cluster_head_receive_and_aggregate(
        nodes
    )

    all_records.extend(records)

    # --------------------------------------------------------
    # Step 4 - CH -> Main CH
    # --------------------------------------------------------

    nodes, records = cluster_head_to_main_ch(
        nodes,
        main_ch_id
    )

    all_records.extend(records)

    # --------------------------------------------------------
    # Step 5 - Main CH -> BS
    # --------------------------------------------------------

    nodes, records = main_ch_to_base_station(
        nodes,
        base_station,
        main_ch_id
    )

    all_records.extend(records)

    communication_table = pd.DataFrame(
        all_records
    )

    return nodes, communication_table


# ============================================================
# 1_08_09 - DISPLAY COMMUNICATION RESULTS
# ============================================================

def display_communication_results(
    nodes,
    communication_table
):

    print()
    print("==============================================")
    print(" 1_08 - COMMUNICATION RESULTS")
    print("==============================================")

    print()
    print("Communication records :", len(
        communication_table
    ))

    if not communication_table.empty:

        print()
        print(
            communication_table.to_string(
                index=False
            )
        )

    print()
    print("----------------------------------------------")

    print(
        "Alive nodes :",
        int(
            np.sum(
                nodes["energy"] > 0
            )
        )
    )

    print(
        "Dead nodes  :",
        int(
            np.sum(
                nodes["energy"] <= 0
            )
        )
    )

    print(
        "Total residual energy :",
        round(
            nodes["energy"].sum(),
            6
        ),
        "J"
    )

    print("----------------------------------------------")


# ============================================================
# 1_08_10 - MODULE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print(" TESTING 1_08 COMMUNICATION")
    print("==============================================")

    # --------------------------------------------------------
    # Deployment
    # --------------------------------------------------------

    nodes, base_station = (
        deployment.deploy_network()
    )

    print(
        "Deployment completed."
    )

    # --------------------------------------------------------
    # ANN1 -> CH selection
    # --------------------------------------------------------

    ann1_result = ann1.run_ann1_ch_selection(
    nodes
    )

    nodes = ann1_result[0]
    ch_indices = ann1_result[1]
    ann1_model = ann1_result[2]

    print(
        "ANN1 CH selection completed."
    )

    # --------------------------------------------------------
    # Clustering
    # --------------------------------------------------------

    clustering_result = clustering.create_clusters(
    nodes,
    ch_indices
    )

    nodes = clustering_result[0]
    clusters = clustering_result[1]

    print(
        "Clustering completed."
    )

    # --------------------------------------------------------
    # ANN2 -> Main CH
    # --------------------------------------------------------

    ann2_result = ann2.run_ann2_main_ch_selection(
    nodes,
    ch_indices
    )

    nodes = ann2_result[0]
    main_ch_id = ann2_result[1]
    ann2_model = ann2_result[2]

    print(
        "ANN2 Main CH selection completed."
    )

    print(
        "Selected Main CH :",
        main_ch_id
    )

    # --------------------------------------------------------
    # Communication
    # --------------------------------------------------------

    nodes, communication_table = (
        run_communication_round(
            nodes,
            base_station,
            main_ch_id
        )
    )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    display_communication_results(
        nodes,
        communication_table
    )

    print()
    print(
        "1_08 communication module "
        "completed successfully."
    )