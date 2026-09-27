# ============================================================
# 1_06 - ANN2 MAIN CLUSTER HEAD SELECTION
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import numpy as np
import pandas as pd

import importlib.util
from pathlib import Path

from sklearn.neural_network import MLPRegressor


# ============================================================
# 1_06_01 - LOAD CONFIGURATION
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
# 1_06_02 - LOAD DEPLOYMENT MODULE
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
# 1_06_03 - LOAD ANN1 MODULE
# ============================================================

ANN1_PATH = (
    CURRENT_FOLDER
    / "1_04_ANN1_CH_Selection.py"
)

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
# 1_06_04 - LOAD CLUSTERING MODULE
# ============================================================

CLUSTERING_PATH = (
    CURRENT_FOLDER
    / "1_05_clustering.py"
)

clustering_spec = importlib.util.spec_from_file_location(
    "clustering",
    CLUSTERING_PATH
)

clustering = importlib.util.module_from_spec(
    clustering_spec
)

clustering_spec.loader.exec_module(
    clustering
)


# ============================================================
# 1_06_05 - CREATE ANN2 INPUT FEATURES
# ============================================================

def create_ann2_features(
    nodes,
    ch_indices
):

    """
    Create ANN2 input features for the selected CHs.

    ANN2 inputs:

        1. CH X position
        2. CH Y position
        3. CH Z position
        4. CH residual energy
        5. CH distance to BS
        6. Cluster size
    """

    ch_nodes = nodes.loc[
        ch_indices
    ].copy()


    features = np.column_stack(

        (

            ch_nodes["x"].to_numpy(),

            ch_nodes["y"].to_numpy(),

            ch_nodes["z"].to_numpy(),

            ch_nodes["energy"].to_numpy(),

            ch_nodes["distanceBS"].to_numpy(),

            ch_nodes["ClusterSize"].to_numpy()

        )

    )


    return (
        ch_nodes,
        features
    )


# ============================================================
# 1_06_06 - CREATE ANN2 TARGET
# ============================================================

def create_ann2_target(
    features_normalized
):

    """
    Create ANN2 training target.

    Target formula:

        0.4 * Energy Score
      + 0.3 * Distance Suitability
      + 0.3 * Cluster Size Suitability

    Higher energy is better.

    Smaller BS distance is better.

    Smaller cluster size is better.
    """

    energy_score = (
        features_normalized[:, 3]
    )


    distance_suitability = (
        1.0
        -
        features_normalized[:, 4]
    )


    cluster_size_suitability = (
        1.0
        -
        features_normalized[:, 5]
    )


    target = (

        0.4 * energy_score

        +

        0.3 * distance_suitability

        +

        0.3 * cluster_size_suitability

    )


    return target


# ============================================================
# 1_06_07 - TRAIN ANN2
# ============================================================

def train_ann2(
    X,
    target
):

    """
    Train ANN2.

    Architecture:

        Input layer  : 6 features
        Hidden layer : 10 neurons
        Output layer : 1 neuron
    """

    ann2 = MLPRegressor(

        hidden_layer_sizes=(10,),

        activation="relu",

        solver="lbfgs",

        max_iter=5000,

        random_state=config.RANDOM_SEED

    )


    ann2.fit(
        X,
        target
    )


    return ann2


# ============================================================
# 1_06_08 - CALCULATE ANN2 SCORES
# ============================================================

def calculate_ann2_scores(
    ann2,
    X
):

    """
    Calculate Main CH suitability score
    for every selected CH.
    """

    scores = ann2.predict(
        X
    )

    return scores


# ============================================================
# 1_06_09 - SELECT MAIN CH
# ============================================================

def select_main_ch(
    ch_indices,
    scores
):

    """
    Select the CH with the highest ANN2 score.
    """

    best_position = np.argmax(
        scores
    )

    main_ch_index = ch_indices[
        best_position
    ]

    return main_ch_index


# ============================================================
# 1_06_10 - ADD ANN2 RESULTS
# ============================================================

def add_ann2_results(
    nodes,
    ch_indices,
    scores,
    main_ch_index
):

    """
    Add ANN2 score and Main CH status
    to the node DataFrame.
    """

    nodes = nodes.copy()


    # --------------------------------------------------------
    # Initialize ANN2 score
    # --------------------------------------------------------

    nodes["ANN2_Score"] = np.nan


    # --------------------------------------------------------
    # Add scores only to CHs
    # --------------------------------------------------------

    nodes.loc[
        ch_indices,
        "ANN2_Score"
    ] = scores


    # --------------------------------------------------------
    # Main CH status
    # --------------------------------------------------------

    nodes["Is_Main_CH"] = False


    nodes.loc[
        main_ch_index,
        "Is_Main_CH"
    ] = True


    return nodes


# ============================================================
# 1_06_11 - MATLAB-STYLE NORMALIZATION
# ============================================================

def minmax_normalize_matlab(X):

    """
    MATLAB-compatible Min-Max normalization.

    If a feature is constant, its normalized value
    is set to 0.5.
    """

    X = np.asarray(
        X,
        dtype=float
    )


    X_min = X.min(
        axis=0
    )


    X_max = X.max(
        axis=0
    )


    X_range = X_max - X_min


    X_norm = np.empty_like(
        X,
        dtype=float
    )


    for j in range(
        X.shape[1]
    ):

        if X_range[j] == 0:

            X_norm[:, j] = 0.5

        else:

            X_norm[:, j] = (

                X[:, j] - X_min[j]

            ) / X_range[j]


    return (
        X_norm,
        X_min,
        X_max
    )


# ============================================================
# 1_06_12 - COMPLETE ANN2 PIPELINE
# ============================================================

def run_ann2_main_ch_selection(
    nodes,
    ch_indices
):

    """
    Complete ANN2 Main CH selection pipeline.

    Steps:

        1. Extract CH information.
        2. Create ANN2 features.
        3. Normalize features.
        4. Create target.
        5. Train ANN2.
        6. Calculate ANN2 scores.
        7. Select highest-scoring CH.
        8. Store results.
    """

    # --------------------------------------------------------
    # Extract CH data and features
    # --------------------------------------------------------

    (
        ch_nodes,
        features

    ) = create_ann2_features(

        nodes,

        ch_indices

    )


    # --------------------------------------------------------
    # Normalize features
    # --------------------------------------------------------

    (
        X_normalized,
        X_min,
        X_max

    ) = minmax_normalize_matlab(
        features
    )


    # --------------------------------------------------------
    # Create target
    # --------------------------------------------------------

    target = create_ann2_target(
        X_normalized
    )


    # --------------------------------------------------------
    # Train ANN2
    # --------------------------------------------------------

    ann2 = train_ann2(

        X_normalized,

        target

    )


    # --------------------------------------------------------
    # Calculate ANN2 scores
    # --------------------------------------------------------

    scores = calculate_ann2_scores(

        ann2,

        X_normalized

    )


    # --------------------------------------------------------
    # Select Main CH
    # --------------------------------------------------------

    main_ch_index = select_main_ch(

        ch_indices,

        scores

    )


    # --------------------------------------------------------
    # Store ANN2 results
    # --------------------------------------------------------

    nodes = add_ann2_results(

        nodes,

        ch_indices,

        scores,

        main_ch_index

    )


    return (

        nodes,

        main_ch_index,

        ann2,

        X_normalized,

        target

    )


# ============================================================
# 1_06_13 - DISPLAY ANN2 RESULTS
# ============================================================

def display_ann2_results(
    nodes,
    ch_indices,
    main_ch_index
):

    """
    Display ANN2 ranking and selected Main CH.
    """

    print()
    print("==============================================")
    print(" 1_06 - ANN2 MAIN CH SELECTION")
    print("==============================================")


    print(
        "Total sensor nodes    :",
        len(nodes)
    )


    print(
        "Number of CHs         :",
        len(ch_indices)
    )


    print(
        "Selected Main CH      :",
        main_ch_index
    )


    print("----------------------------------------------")

    print(
        "ANN2 CH RANKING"
    )

    print("----------------------------------------------")


    ch_ranking = nodes.loc[
        ch_indices
    ].sort_values(
        by="ANN2_Score",
        ascending=False
    )


    print(

        ch_ranking[

            [

                "NodeID",

                "x",

                "y",

                "z",

                "energy",

                "distanceBS",

                "ClusterSize",

                "ANN2_Score",

                "Is_Main_CH"

            ]

        ].to_string(
            index=False
        )

    )


    print("----------------------------------------------")


    # ========================================================
    # Display Main CH details
    # ========================================================

    main_ch = nodes.loc[
        main_ch_index
    ]


    print(
        "MAIN CH DETAILS"
    )

    print("----------------------------------------------")


    print(
        "Node ID              :",
        int(main_ch["NodeID"])
    )


    print(
        "X position           :",
        round(
            main_ch["x"],
            3
        )
    )


    print(
        "Y position           :",
        round(
            main_ch["y"],
            3
        )
    )


    print(
        "Z position           :",
        round(
            main_ch["z"],
            3
        )
    )


    print(
        "Residual energy      :",
        round(
            main_ch["energy"],
            6
        ),
        "J"
    )


    print(
        "Distance to BS       :",
        round(
            main_ch["distanceBS"],
            3
        ),
        "m"
    )


    print(
        "Cluster size         :",
        int(
            main_ch["ClusterSize"]
        )
    )


    print(
        "ANN2 score           :",
        round(
            main_ch["ANN2_Score"],
            6
        )
    )


    print("----------------------------------------------")

    print(
        "ANN2 Main CH selection completed."
    )


# ============================================================
# 1_06_14 - MODULE TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Deploy network
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
        ann1_X,
        ann1_target

    ) = ann1.run_ann1_ch_selection(
        nodes
    )


    # --------------------------------------------------------
    # Clustering
    # --------------------------------------------------------

    (
        nodes,
        clusters,
        cluster_sizes,
        average_cluster_energy

    ) = clustering.create_clusters(

        nodes,

        ch_indices

    )


    # --------------------------------------------------------
    # ANN2 Main CH selection
    # --------------------------------------------------------

    (
        nodes,
        main_ch_index,
        ann2_model,
        ann2_X,
        ann2_target

    ) = run_ann2_main_ch_selection(

        nodes,

        ch_indices

    )


    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    display_ann2_results(

        nodes,

        ch_indices,

        main_ch_index

    )