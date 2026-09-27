# ============================================================
# 1_02 - NETWORK DEPLOYMENT
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import numpy as np
import pandas as pd
import importlib.util
from pathlib import Path


# ============================================================
# 1_02_01 - LOAD CONFIGURATION
# ============================================================

CURRENT_FOLDER = Path(__file__).resolve().parent

CONFIG_PATH = CURRENT_FOLDER / "1_01_config.py"

spec = importlib.util.spec_from_file_location(
    "config",
    CONFIG_PATH
)

config = importlib.util.module_from_spec(spec)

spec.loader.exec_module(config)


# ============================================================
# 1_02_02 - CREATE SENSOR NODES
# ============================================================

def create_nodes():

    """
    Create the WSN sensor nodes.

    Returns
    -------
    pandas.DataFrame
        Sensor-node information.
    """

    # --------------------------------------------------------
    # Set random seed
    # --------------------------------------------------------

    np.random.seed(config.RANDOM_SEED)


    # --------------------------------------------------------
    # Generate random 3D coordinates
    # --------------------------------------------------------

    x = np.random.uniform(
        0,
        config.AREA_X,
        config.SN
    )

    y = np.random.uniform(
        0,
        config.AREA_Y,
        config.SN
    )

    z = np.random.uniform(
        0,
        config.AREA_Z,
        config.SN
    )


    # --------------------------------------------------------
    # Initial energy
    # --------------------------------------------------------

    energy = np.full(
        config.SN,
        config.INITIAL_ENERGY
    )


    # --------------------------------------------------------
    # Calculate distance from Base Station
    # --------------------------------------------------------

    distance_bs = np.sqrt(
        (x - config.BS_X) ** 2
        +
        (y - config.BS_Y) ** 2
        +
        (z - config.BS_Z) ** 2
    )


    # ========================================================
    # Create DataFrame
    # ========================================================

    nodes = pd.DataFrame({

        "NodeID": np.arange(
            config.SN
        ),

        "x": x,

        "y": y,

        "z": z,

        "energy": energy,

        "distanceBS": distance_bs
    })


    return nodes


# ============================================================
# 1_02_03 - CREATE BASE STATION
# ============================================================

def create_base_station():

    """
    Create Base Station information.

    Returns
    -------
    dict
        Base Station coordinates.
    """

    base_station = {

        "x": config.BS_X,

        "y": config.BS_Y,

        "z": config.BS_Z
    }

    return base_station


# ============================================================
# 1_02_04 - DEPLOY COMPLETE NETWORK
# ============================================================

def deploy_network():

    """
    Create the complete WSN deployment.

    Returns
    -------
    nodes : pandas.DataFrame
        Sensor-node information.

    base_station : dict
        Base Station information.
    """

    nodes = create_nodes()

    base_station = create_base_station()

    return nodes, base_station


# ============================================================
# 1_02_05 - DISPLAY NETWORK INFORMATION
# ============================================================

def display_network_information(
    nodes,
    base_station
):

    print()
    print("==============================================")
    print(" 1_02 - NETWORK DEPLOYMENT")
    print("==============================================")

    print(
        "Number of nodes       :",
        len(nodes)
    )

    print(
        "Network dimensions    :",
        config.AREA_X,
        "x",
        config.AREA_Y,
        "x",
        config.AREA_Z,
        "m"
    )

    print(
        "Initial energy        :",
        config.INITIAL_ENERGY,
        "J"
    )

    print(
        "Base Station          :",
        (
            base_station["x"],
            base_station["y"],
            base_station["z"]
        )
    )

    print("----------------------------------------------")

    print("First 5 sensor nodes:")

    print(
        nodes.head()
    )

    print("----------------------------------------------")

    print(
        "Minimum distance to BS :",
        round(
            nodes["distanceBS"].min(),
            3
        ),
        "m"
    )

    print(
        "Maximum distance to BS :",
        round(
            nodes["distanceBS"].max(),
            3
        ),
        "m"
    )

    print("----------------------------------------------")

    print(
        "Total initial energy   :",
        round(
            nodes["energy"].sum(),
            3
        ),
        "J"
    )

    print("----------------------------------------------")

    print(
        "Network deployment completed successfully."
    )


# ============================================================
# 1_02_06 - MODULE TEST
# ============================================================

if __name__ == "__main__":

    nodes, base_station = deploy_network()

    display_network_information(
        nodes,
        base_station
    )