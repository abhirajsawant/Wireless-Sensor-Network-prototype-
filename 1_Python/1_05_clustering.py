# ============================================================
# 1_05 - CLUSTERING
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import numpy as np
import pandas as pd

import importlib.util
from pathlib import Path


# ============================================================
# 1_05_01 - LOAD CONFIGURATION
# ============================================================

CURRENT_FOLDER = Path(__file__).resolve().parent

CONFIG_PATH = CURRENT_FOLDER / "1_01_config.py"

config_spec = importlib.util.spec_from_file_location(
    "config",
    CONFIG_PATH
)

config = importlib.util.module_from_spec(
    config_spec
)

config_spec.loader.exec_module(
    config
)


# ============================================================
# 1_05_02 - LOAD DEPLOYMENT MODULE
# ============================================================

DEPLOYMENT_PATH = CURRENT_FOLDER / "1_02_deployment.py"

deployment_spec = importlib.util.spec_from_file_location(
    "deployment",
    DEPLOYMENT_PATH
)

deployment = importlib.util.module_from_spec(
    deployment_spec
)

deployment_spec.loader.exec_module(
    deployment
)


# ============================================================
# 1_05_03 - LOAD ANN1 MODULE
# ============================================================

ANN1_PATH = CURRENT_FOLDER / "1_04_ANN1_CH_Selection.py"

ann1_spec = importlib.util.spec_from_file_location(
    "ann1",
    ANN1_PATH
)

ann1 = importlib.util.module_from_spec(
    ann1_spec
)

ann1_spec.loader.exec_module(
    ann1
)


# ============================================================
# 1_05_04 - CALCULATE DISTANCE BETWEEN NODES
# ============================================================

def calculate_3d_distance(
    node_a,
    node_b
):

    """
    Calculate Euclidean distance between two
    3D nodes.

    Formula:

        d = sqrt(
            (x1-x2)^2
          + (y1-y2)^2
          + (z1-z2)^2
        )
    """

    distance = np.sqrt(

        (node_a["x"] - node_b["x"]) ** 2

        +

        (node_a["y"] - node_b["y"]) ** 2

        +

        (node_a["z"] - node_b["z"]) ** 2

    )

    return distance


# ============================================================
# 1_05_05 - ASSIGN NODES TO NEAREST CH
# ============================================================

def assign_nodes_to_clusters(
    nodes,
    ch_indices
):

    """
    Assign every non-CH node to its nearest CH.

    CH nodes are assigned to their own cluster.

    Returns
    -------
    nodes : pandas.DataFrame
        Nodes with ClusterID and CH_ID.

    clusters : dict
        Dictionary containing nodes belonging
        to each cluster.
    """

    nodes = nodes.copy()


    # --------------------------------------------------------
    # Check that CHs exist
    # --------------------------------------------------------

    if len(ch_indices) == 0:

        raise ValueError(
            "No Cluster Heads were selected."
        )


    # --------------------------------------------------------
    # Create cluster columns
    # --------------------------------------------------------

    nodes["ClusterID"] = -1

    nodes["CH_ID"] = -1


    # ========================================================
    # Assign every node
    # ========================================================

    for node_index in nodes.index:

        # ----------------------------------------------------
        # If node itself is a CH
        # ----------------------------------------------------

        if node_index in ch_indices:

            nodes.loc[
                node_index,
                "ClusterID"
            ] = node_index

            nodes.loc[
                node_index,
                "CH_ID"
            ] = node_index

            continue


        # ----------------------------------------------------
        # Calculate distance to every CH
        # ----------------------------------------------------

        distances = []

        for ch_index in ch_indices:

            distance = calculate_3d_distance(

                nodes.loc[node_index],

                nodes.loc[ch_index]

            )

            distances.append(
                distance
            )


        # ----------------------------------------------------
        # Find nearest CH
        # ----------------------------------------------------

        nearest_position = np.argmin(
            distances
        )

        nearest_ch_index = ch_indices[
            nearest_position
        ]


        # ----------------------------------------------------
        # Assign node to nearest CH
        # ----------------------------------------------------

        nodes.loc[
            node_index,
            "ClusterID"
        ] = nearest_ch_index

        nodes.loc[
            node_index,
            "CH_ID"
        ] = nearest_ch_index


    # ========================================================
    # Build cluster dictionary
    # ========================================================

    clusters = {}

    for ch_index in ch_indices:

        cluster_nodes = nodes[
            nodes["ClusterID"] == ch_index
        ].copy()

        clusters[ch_index] = cluster_nodes


    return (
        nodes,
        clusters
    )


# ============================================================
# 1_05_06 - CALCULATE CLUSTER SIZE
# ============================================================

def calculate_cluster_sizes(
    nodes,
    ch_indices
):

    """
    Calculate the number of nodes in every cluster.
    """

    cluster_sizes = {}


    for ch_index in ch_indices:

        cluster_size = int(
            np.sum(
                nodes["ClusterID"] == ch_index
            )
        )

        cluster_sizes[ch_index] = cluster_size


    return cluster_sizes


# ============================================================
# 1_05_07 - CALCULATE AVERAGE CLUSTER ENERGY
# ============================================================

def calculate_average_cluster_energy(
    nodes,
    ch_indices
):

    """
    Calculate the actual average residual energy
    of every cluster.

    The average is calculated from the nodes currently
    belonging to each cluster.
    """

    average_cluster_energy = {}


    for ch_index in ch_indices:

        cluster_nodes = nodes[
            nodes["ClusterID"] == ch_index
        ]


        if len(cluster_nodes) == 0:

            average_energy = 0.0

        else:

            average_energy = (
                cluster_nodes["energy"].mean()
            )


        average_cluster_energy[ch_index] = (
            average_energy
        )


    return average_cluster_energy


# ============================================================
# 1_05_08 - STORE CLUSTER ENERGY IN NODE TABLE
# ============================================================

def add_cluster_information(
    nodes,
    ch_indices,
    cluster_sizes,
    average_cluster_energy
):

    """
    Add cluster size and average cluster energy
    to every node.
    """

    nodes = nodes.copy()


    # --------------------------------------------------------
    # Cluster size
    # --------------------------------------------------------

    nodes["ClusterSize"] = nodes[
        "CH_ID"
    ].map(
        cluster_sizes
    )


    # --------------------------------------------------------
    # Average cluster energy
    # --------------------------------------------------------

    nodes["avgClusterEnergy"] = nodes[
        "CH_ID"
    ].map(
        average_cluster_energy
    )


    return nodes


# ============================================================
# 1_05_09 - COMPLETE CLUSTERING PIPELINE
# ============================================================

def create_clusters(
    nodes,
    ch_indices
):

    """
    Complete clustering pipeline.

    Steps:

        1. Assign nodes to nearest CH.
        2. Calculate cluster size.
        3. Calculate average cluster energy.
        4. Store information in node table.

    Returns
    -------
    nodes : pandas.DataFrame

    clusters : dict

    cluster_sizes : dict

    average_cluster_energy : dict
    """

    # --------------------------------------------------------
    # Assign nodes
    # --------------------------------------------------------

    (
        nodes,
        clusters
    ) = assign_nodes_to_clusters(

        nodes,

        ch_indices

    )


    # --------------------------------------------------------
    # Cluster sizes
    # --------------------------------------------------------

    cluster_sizes = calculate_cluster_sizes(

        nodes,

        ch_indices

    )


    # --------------------------------------------------------
    # Average cluster energy
    # --------------------------------------------------------

    average_cluster_energy = (
        calculate_average_cluster_energy(

            nodes,

            ch_indices

        )
    )


    # --------------------------------------------------------
    # Store cluster information
    # --------------------------------------------------------

    nodes = add_cluster_information(

        nodes,

        ch_indices,

        cluster_sizes,

        average_cluster_energy

    )


    return (

        nodes,

        clusters,

        cluster_sizes,

        average_cluster_energy

    )


# ============================================================
# 1_05_10 - DISPLAY CLUSTER INFORMATION
# ============================================================

def display_cluster_information(
    nodes,
    ch_indices,
    cluster_sizes,
    average_cluster_energy
):

    """
    Display complete cluster information.
    """

    print()
    print("==============================================")
    print(" 1_05 - CLUSTERING")
    print("==============================================")

    print(
        "Total sensor nodes    :",
        len(nodes)
    )

    print(
        "Number of CHs         :",
        len(ch_indices)
    )

    print("----------------------------------------------")

    print(
        "CLUSTER INFORMATION"
    )

    print("----------------------------------------------")


    # ========================================================
    # Display each cluster
    # ========================================================

    for cluster_number, ch_index in enumerate(
        ch_indices,
        start=1
    ):

        size = cluster_sizes[
            ch_index
        ]

        avg_energy = average_cluster_energy[
            ch_index
        ]


        print(
            f"Cluster {cluster_number:02d}"
        )

        print(
            "  CH Node ID          :",
            ch_index
        )

        print(
            "  Cluster size        :",
            size
        )

        print(
            "  Average energy      :",
            round(
                avg_energy,
                6
            ),
            "J"
        )

        print()


    print("----------------------------------------------")

    print(
        "NODE → CH ASSIGNMENTS"
    )

    print("----------------------------------------------")


    # ========================================================
    # Display node assignments
    # ========================================================

    display_columns = [

        "NodeID",

        "CH_ID",

        "ClusterID",

        "ClusterSize",

        "energy",

        "avgClusterEnergy"

    ]


    print(
        nodes[
            display_columns
        ]
        .sort_values(
            by="NodeID"
        )
        .to_string(
            index=False
        )
    )


    print("----------------------------------------------")

    print(
        "Clustering completed successfully."
    )


# ============================================================
# 1_05_11 - MODULE TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Create network
    # --------------------------------------------------------

    nodes, base_station = (
        deployment.deploy_network()
    )


    # --------------------------------------------------------
    # ANN1 CH selection
    # --------------------------------------------------------

    (
        nodes,
        ch_indices,
        ann1_model,
        X_normalized,
        target

    ) = ann1.run_ann1_ch_selection(
        nodes
    )


    # --------------------------------------------------------
    # Create clusters
    # --------------------------------------------------------

    (
        nodes,
        clusters,
        cluster_sizes,
        average_cluster_energy

    ) = create_clusters(

        nodes,

        ch_indices

    )


    # --------------------------------------------------------
    # Display cluster information
    # --------------------------------------------------------

    display_cluster_information(

        nodes,

        ch_indices,

        cluster_sizes,

        average_cluster_energy

    )