# ============================================================
# 1_04 - ANN1 CLUSTER HEAD SELECTION
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import numpy as np
import pandas as pd

import importlib.util
from pathlib import Path

from sklearn.neural_network import MLPRegressor


# ============================================================
# 1_04_01 - LOAD CONFIGURATION
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
# 1_04_02 - LOAD DEPLOYMENT MODULE
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
# 1_04_03 - MATLAB-STYLE MIN-MAX NORMALIZATION
# ============================================================

def minmax_normalize_matlab(X):

    """
    Perform Min-Max normalization using the same
    constant-feature behavior as the MATLAB prototype.

    Normalization:

        X_norm = (X - X_min) / (X_max - X_min)

    If a feature has the same minimum and maximum value,
    MATLAB prototype behavior is:

        X_norm = 0.5
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


    # --------------------------------------------------------
    # Normalize every feature
    # --------------------------------------------------------

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
# 1_04_04 - CREATE ANN1 INPUT FEATURES
# ============================================================

def create_ann1_features(nodes):

    """
    Create the six ANN1 input features.

    ANN1 inputs:

        1. X position
        2. Y position
        3. Z position
        4. Energy
        5. Distance from BS
        6. Average cluster energy

    At the initial deployment stage, average cluster
    energy is initialized using the node energy.

    Returns
    -------
    numpy.ndarray
        ANN1 feature matrix.
    """

    # --------------------------------------------------------
    # Average cluster energy
    # --------------------------------------------------------

    if "avgClusterEnergy" in nodes.columns:

        average_cluster_energy = (
            nodes["avgClusterEnergy"].to_numpy()
        )

    else:

        average_cluster_energy = (
            nodes["energy"].to_numpy()
        )


    # --------------------------------------------------------
    # Six ANN1 inputs
    # --------------------------------------------------------

    features = np.column_stack(

        (

            nodes["x"].to_numpy(),

            nodes["y"].to_numpy(),

            nodes["z"].to_numpy(),

            nodes["energy"].to_numpy(),

            nodes["distanceBS"].to_numpy(),

            average_cluster_energy

        )

    )


    return features


# ============================================================
# 1_04_05 - CREATE ANN1 TRAINING TARGET
# ============================================================

def create_ann1_target(
    features_normalized
):

    """
    Create the ANN1 training target.

    Target formula:

        0.4 * Energy Score
      + 0.3 * Distance Suitability
      + 0.3 * Cluster Energy Score

    Higher energy is better.

    Smaller distance from BS is better.
    Therefore distance suitability is:

        1 - normalized distance

    Higher average cluster energy is better.
    """

    energy_score = (
        features_normalized[:, 3]
    )

    distance_suitability = (
        1.0
        -
        features_normalized[:, 4]
    )

    cluster_energy_score = (
        features_normalized[:, 5]
    )


    target = (

        0.4 * energy_score

        +

        0.3 * distance_suitability

        +

        0.3 * cluster_energy_score

    )


    return target


# ============================================================
# 1_04_06 - TRAIN ANN1
# ============================================================

def train_ann1(
    X,
    target
):

    """
    Train ANN1.

    Architecture:

        Input layer  : 6 features
        Hidden layer : 10 neurons
        Output layer : 1 neuron
    """

    ann1 = MLPRegressor(

        hidden_layer_sizes=(10,),

        activation="relu",

        solver="lbfgs",

        max_iter=5000,

        random_state=config.RANDOM_SEED

    )


    ann1.fit(
        X,
        target
    )


    return ann1


# ============================================================
# 1_04_07 - CALCULATE ANN1 SUITABILITY SCORES
# ============================================================

def calculate_ann1_scores(
    ann1,
    X
):

    """
    Calculate ANN1 suitability score for every node.
    """

    scores = ann1.predict(
        X
    )

    return scores


# ============================================================
# 1_04_08 - SELECT CLUSTER HEADS
# ============================================================

def select_cluster_heads(
    nodes,
    scores
):

    """
    Select the highest-scoring nodes as Cluster Heads.

    Number of CHs:

        floor(CH probability * number of nodes)
    """

    number_of_nodes = len(
        nodes
    )

    number_of_ch = int(

        np.floor(

            config.CH_PROBABILITY
            *
            number_of_nodes

        )

    )


    # --------------------------------------------------------
    # Sort scores from highest to lowest
    # --------------------------------------------------------

    sorted_indices = np.argsort(
        scores
    )[::-1]


    # --------------------------------------------------------
    # Select top-scoring nodes
    # --------------------------------------------------------

    ch_indices = sorted_indices[
        :number_of_ch
    ]


    return ch_indices


# ============================================================
# 1_04_09 - ADD ANN1 RESULTS TO NODE TABLE
# ============================================================

def add_ann1_results(
    nodes,
    scores,
    ch_indices
):

    """
    Add ANN1 suitability score and CH status
    to the node DataFrame.
    """

    nodes = nodes.copy()


    # --------------------------------------------------------
    # ANN1 score
    # --------------------------------------------------------

    nodes["ANN1_Score"] = scores


    # --------------------------------------------------------
    # CH status
    # --------------------------------------------------------

    nodes["Is_CH"] = False

    nodes.loc[
        ch_indices,
        "Is_CH"
    ] = True


    return nodes


# ============================================================
# 1_04_10 - COMPLETE ANN1 PIPELINE
# ============================================================

def run_ann1_ch_selection(
    nodes
):

    """
    Complete ANN1 Cluster Head selection pipeline.

    Returns
    -------
    nodes : pandas.DataFrame
        Nodes containing ANN1 scores and CH status.

    ch_indices : numpy.ndarray
        Indices of selected Cluster Heads.

    ann1 : MLPRegressor
        Trained ANN1 model.

    X_normalized : numpy.ndarray
        Normalized ANN1 input data.

    target : numpy.ndarray
        ANN1 training target.
    """

    # --------------------------------------------------------
    # Create ANN1 features
    # --------------------------------------------------------

    features = create_ann1_features(
        nodes
    )


    # --------------------------------------------------------
    # Normalize ANN1 features
    # --------------------------------------------------------

    (
        X_normalized,
        X_min,
        X_max
    ) = minmax_normalize_matlab(
        features
    )


    # --------------------------------------------------------
    # Create training target
    # --------------------------------------------------------

    target = create_ann1_target(
        X_normalized
    )


    # --------------------------------------------------------
    # Train ANN1
    # --------------------------------------------------------

    ann1 = train_ann1(
        X_normalized,
        target
    )


    # --------------------------------------------------------
    # Calculate suitability scores
    # --------------------------------------------------------

    scores = calculate_ann1_scores(
        ann1,
        X_normalized
    )


    # --------------------------------------------------------
    # Select CHs
    # --------------------------------------------------------

    ch_indices = select_cluster_heads(
        nodes,
        scores
    )


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    nodes = add_ann1_results(
        nodes,
        scores,
        ch_indices
    )


    return (
        nodes,
        ch_indices,
        ann1,
        X_normalized,
        target
    )


# ============================================================
# 1_04_11 - DISPLAY CH SELECTION
# ============================================================

def display_ch_selection(
    nodes,
    ch_indices
):

    """
    Display all ANN1 scores and selected CHs.
    """

    print()
    print("==============================================")
    print(" 1_04 - ANN1 CLUSTER HEAD SELECTION")
    print("==============================================")


    # --------------------------------------------------------
    # Number of CHs
    # --------------------------------------------------------

    print(
        "Total sensor nodes    :",
        len(nodes)
    )

    print(
        "CH probability        :",
        config.CH_PROBABILITY
    )

    print(
        "Number of CHs         :",
        len(ch_indices)
    )

    print("----------------------------------------------")


    # ========================================================
    # Display all nodes sorted by ANN1 score
    # ========================================================

    ranking = nodes.sort_values(
        by="ANN1_Score",
        ascending=False
    )


    print(
        "ANN1 NODE RANKING"
    )

    print("----------------------------------------------")

    print(
        ranking[
            [
                "NodeID",
                "energy",
                "distanceBS",
                "ANN1_Score",
                "Is_CH"
            ]
        ].to_string(
            index=False
        )
    )


    print("----------------------------------------------")


    # ========================================================
    # Display selected CHs
    # ========================================================

    selected_chs = nodes.loc[
        nodes["Is_CH"] == True
    ].sort_values(
        by="ANN1_Score",
        ascending=False
    )


    print(
        "SELECTED CLUSTER HEADS"
    )

    print("----------------------------------------------")

    print(
        selected_chs[
            [
                "NodeID",
                "x",
                "y",
                "z",
                "energy",
                "distanceBS",
                "ANN1_Score"
            ]
        ].to_string(
            index=False
        )
    )

    print("----------------------------------------------")

    print(
        "ANN1 Cluster Head selection completed."
    )


# ============================================================
# 1_04_12 - MODULE TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Create network
    # --------------------------------------------------------

    nodes, base_station = (
        deployment.deploy_network()
    )


    # --------------------------------------------------------
    # Run ANN1
    # --------------------------------------------------------

    (
        nodes,
        ch_indices,
        ann1,
        X_normalized,
        target
    ) = run_ann1_ch_selection(
        nodes
    )


    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    display_ch_selection(
        nodes,
        ch_indices
    )