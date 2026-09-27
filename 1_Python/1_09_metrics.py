# ============================================================
# 1_09 - PERFORMANCE METRICS
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import numpy as np
import pandas as pd
import importlib.util
from pathlib import Path


# ============================================================
# 1_09_01 - LOAD CONFIGURATION
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


# ============================================================
# 1_09_02 - BASIC NODE METRICS
# ============================================================

def calculate_node_metrics(nodes):

    total_nodes = len(nodes)

    alive_nodes = int(
        np.sum(nodes["energy"] > 0)
    )

    dead_nodes = (
        total_nodes -
        alive_nodes
    )

    total_residual_energy = float(
        nodes["energy"].sum()
    )

    average_residual_energy = (
        total_residual_energy / total_nodes
        if total_nodes > 0
        else 0.0
    )

    return {

        "TotalNodes":
            total_nodes,

        "AliveNodes":
            alive_nodes,

        "DeadNodes":
            dead_nodes,

        "ResidualEnergy":
            total_residual_energy,

        "AverageResidualEnergy":
            average_residual_energy
    }


# ============================================================
# 1_09_03 - ENERGY CONSUMPTION
# ============================================================

def calculate_energy_consumption(
    previous_nodes,
    current_nodes
):

    previous_energy = float(
        previous_nodes["energy"].sum()
    )

    current_energy = float(
        current_nodes["energy"].sum()
    )

    energy_consumed = (
        previous_energy -
        current_energy
    )

    # Prevent a negative value because of
    # numerical precision.

    energy_consumed = max(
        energy_consumed,
        0.0
    )

    return energy_consumed


# ============================================================
# 1_09_04 - COMMUNICATION PACKET METRICS
# ============================================================

def calculate_packet_metrics(
    communication_table
):

    if communication_table is None:

        return {

            "NodeToCHPackets": 0,

            "CHToMainCHPackets": 0,

            "MainCHToBSPackets": 0,

            "TotalCommunicationRecords": 0,

            "ThroughputBits": 0
        }

    if communication_table.empty:

        return {

            "NodeToCHPackets": 0,

            "CHToMainCHPackets": 0,

            "MainCHToBSPackets": 0,

            "TotalCommunicationRecords": 0,

            "ThroughputBits": 0
        }


    # --------------------------------------------------------
    # Normal node -> CH
    # --------------------------------------------------------

    node_to_ch = int(
        np.sum(
            communication_table["Link"]
            == "Node_to_CH"
        )
    )


    # --------------------------------------------------------
    # CH -> Main CH
    # --------------------------------------------------------

    ch_to_main_ch = int(
        np.sum(
            communication_table["Link"]
            == "CH_to_Main_CH"
        )
    )


    # --------------------------------------------------------
    # Main CH -> Base Station
    # --------------------------------------------------------

    main_ch_to_bs = int(
        np.sum(
            communication_table["Link"]
            == "Main_CH_to_BS"
        )
    )


    # --------------------------------------------------------
    # Throughput
    # --------------------------------------------------------

    throughput_bits = (
        main_ch_to_bs *
        energy_model.PACKET_SIZE
    )


    return {

        "NodeToCHPackets":
            node_to_ch,

        "CHToMainCHPackets":
            ch_to_main_ch,

        "MainCHToBSPackets":
            main_ch_to_bs,

        "TotalCommunicationRecords":
            len(communication_table),

        "ThroughputBits":
            throughput_bits
    }


# ============================================================
# 1_09_05 - PACKET DELIVERY RATIO
# ============================================================

def calculate_pdr(
    packets_generated,
    packets_delivered
):

    packets_generated = max(
        int(packets_generated),
        0
    )

    packets_delivered = max(
        int(packets_delivered),
        0
    )

    if packets_generated == 0:

        return 0.0

    pdr = (
        packets_delivered /
        packets_generated
    )

    # Keep PDR within 0-1.

    pdr = min(
        max(pdr, 0.0),
        1.0
    )

    return pdr


# ============================================================
# 1_09_06 - FIRST NODE DEATH
# ============================================================

def calculate_fnd(
    round_number,
    nodes,
    current_fnd
):

    dead_nodes = int(
        np.sum(
            nodes["energy"] <= 0
        )
    )

    if (
        dead_nodes > 0
        and current_fnd is None
    ):

        return round_number

    return current_fnd


# ============================================================
# 1_09_07 - HALF NODE DEATH
# ============================================================

def calculate_hnd(
    round_number,
    nodes,
    current_hnd
):

    total_nodes = len(nodes)

    dead_nodes = int(
        np.sum(
            nodes["energy"] <= 0
        )
    )

    half_nodes = total_nodes / 2

    if (
        dead_nodes >= half_nodes
        and current_hnd is None
    ):

        return round_number

    return current_hnd


# ============================================================
# 1_09_08 - LAST NODE DEATH
# ============================================================

def calculate_lnd(
    round_number,
    nodes,
    current_lnd
):

    alive_nodes = int(
        np.sum(
            nodes["energy"] > 0
        )
    )

    if (
        alive_nodes == 0
        and current_lnd is None
    ):

        return round_number

    return current_lnd


# ============================================================
# 1_09_09 - NETWORK LIFETIME
# ============================================================

def calculate_network_lifetime(
    current_lnd
):

    if current_lnd is None:

        return 0

    return current_lnd


# ============================================================
# 1_09_10 - CREATE ROUND METRICS
# ============================================================

def calculate_round_metrics(
    round_number,
    previous_nodes,
    current_nodes,
    communication_table,
    current_fnd=None,
    current_hnd=None,
    current_lnd=None
):

    # --------------------------------------------------------
    # Node metrics
    # --------------------------------------------------------

    node_metrics = calculate_node_metrics(
        current_nodes
    )


    # --------------------------------------------------------
    # Energy consumption
    # --------------------------------------------------------

    energy_consumed = (
        calculate_energy_consumption(
            previous_nodes,
            current_nodes
        )
    )


    # --------------------------------------------------------
    # Packet metrics
    # --------------------------------------------------------

    packet_metrics = (
        calculate_packet_metrics(
            communication_table
        )
    )


    # --------------------------------------------------------
    # Lifetime metrics
    # --------------------------------------------------------

    fnd = calculate_fnd(
        round_number,
        current_nodes,
        current_fnd
    )

    hnd = calculate_hnd(
        round_number,
        current_nodes,
        current_hnd
    )

    lnd = calculate_lnd(
        round_number,
        current_nodes,
        current_lnd
    )


    # --------------------------------------------------------
    # Create one complete record
    # --------------------------------------------------------

    metrics = {

        "Round":
            round_number,

        "TotalNodes":
            node_metrics["TotalNodes"],

        "AliveNodes":
            node_metrics["AliveNodes"],

        "DeadNodes":
            node_metrics["DeadNodes"],

        "ResidualEnergy":
            node_metrics["ResidualEnergy"],

        "AverageResidualEnergy":
            node_metrics[
                "AverageResidualEnergy"
            ],

        "EnergyConsumed":
            energy_consumed,

        "NodeToCHPackets":
            packet_metrics[
                "NodeToCHPackets"
            ],

        "CHToMainCHPackets":
            packet_metrics[
                "CHToMainCHPackets"
            ],

        "MainCHToBSPackets":
            packet_metrics[
                "MainCHToBSPackets"
            ],

        "ThroughputBits":
            packet_metrics[
                "ThroughputBits"
            ],

        "FND":
            fnd,

        "HND":
            hnd,

        "LND":
            lnd
    }


    return (
        metrics,
        fnd,
        hnd,
        lnd
    )


# ============================================================
# 1_09_11 - CREATE METRICS HISTORY
# ============================================================

def create_metrics_history():

    return []


# ============================================================
# 1_09_12 - ADD ROUND TO HISTORY
# ============================================================

def add_metrics_to_history(
    history,
    metrics
):

    history.append(
        metrics.copy()
    )

    return history


# ============================================================
# 1_09_13 - CONVERT HISTORY TO DATAFRAME
# ============================================================

def history_to_dataframe(
    history
):

    if not history:

        return pd.DataFrame()

    return pd.DataFrame(
        history
    )


# ============================================================
# 1_09_14 - DISPLAY CURRENT METRICS
# ============================================================

def display_metrics(metrics):

    print()
    print("==============================================")
    print(" ROUND PERFORMANCE METRICS")
    print("==============================================")

    print(
        "Round                 :",
        metrics["Round"]
    )

    print(
        "Total nodes           :",
        metrics["TotalNodes"]
    )

    print(
        "Alive nodes           :",
        metrics["AliveNodes"]
    )

    print(
        "Dead nodes            :",
        metrics["DeadNodes"]
    )

    print(
        "Residual energy       :",
        round(
            metrics["ResidualEnergy"],
            6
        ),
        "J"
    )

    print(
        "Average residual      :",
        round(
            metrics["AverageResidualEnergy"],
            6
        ),
        "J"
    )

    print(
        "Energy consumed       :",
        round(
            metrics["EnergyConsumed"],
            6
        ),
        "J"
    )

    print(
        "Node -> CH packets    :",
        metrics["NodeToCHPackets"]
    )

    print(
        "CH -> Main CH packets :",
        metrics["CHToMainCHPackets"]
    )

    print(
        "Main CH -> BS packets :",
        metrics["MainCHToBSPackets"]
    )

    print(
        "Throughput            :",
        metrics["ThroughputBits"],
        "bits"
    )

    print(
        "FND                   :",
        metrics["FND"]
    )

    print(
        "HND                   :",
        metrics["HND"]
    )

    print(
        "LND                   :",
        metrics["LND"]
    )

    print("----------------------------------------------")


# ============================================================
# 1_09_15 - DISPLAY METRICS HISTORY
# ============================================================

def display_metrics_history(
    history_dataframe
):

    if history_dataframe.empty:

        print()
        print(
            "No metrics history available."
        )

        return


    print()
    print("==============================================")
    print(" METRICS HISTORY")
    print("==============================================")

    print(
        history_dataframe.to_string(
            index=False
        )
    )


# ============================================================
# 1_09_16 - MODULE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print(" TESTING 1_09 METRICS")
    print("==============================================")


    # --------------------------------------------------------
    # Create a small artificial network
    # for testing the metric calculations.
    # --------------------------------------------------------

    previous_nodes = pd.DataFrame({

        "NodeID": [0, 1, 2, 3, 4],

        "energy": [
            0.50,
            0.45,
            0.40,
            0.35,
            0.30
        ]
    })


    current_nodes = pd.DataFrame({

        "NodeID": [0, 1, 2, 3, 4],

        "energy": [
            0.48,
            0.43,
            0.00,
            0.32,
            0.00
        ]
    })


    # --------------------------------------------------------
    # Artificial communication records
    # --------------------------------------------------------

    communication_table = pd.DataFrame({

        "Sender": [
            0,
            1,
            3,
            0
        ],

        "Receiver": [
            10,
            10,
            11,
            "Base Station"
        ],

        "Link": [
            "Node_to_CH",
            "Node_to_CH",
            "CH_to_Main_CH",
            "Main_CH_to_BS"
        ],

        "Distance": [
            20.0,
            30.0,
            40.0,
            50.0
        ],

        "EnergyConsumed": [
            0.001,
            0.001,
            0.002,
            0.003
        ]
    })


    # --------------------------------------------------------
    # Test FND / HND / LND
    # --------------------------------------------------------

    fnd = None
    hnd = None
    lnd = None


    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    metrics, fnd, hnd, lnd = (
        calculate_round_metrics(

            round_number=10,

            previous_nodes=
                previous_nodes,

            current_nodes=
                current_nodes,

            communication_table=
                communication_table,

            current_fnd=
                fnd,

            current_hnd=
                hnd,

            current_lnd=
                lnd
        )
    )


    # --------------------------------------------------------
    # Display metrics
    # --------------------------------------------------------

    display_metrics(
        metrics
    )


    # --------------------------------------------------------
    # Test history
    # --------------------------------------------------------

    history = (
        create_metrics_history()
    )

    history = (
        add_metrics_to_history(
            history,
            metrics
        )
    )

    history_dataframe = (
        history_to_dataframe(
            history
        )
    )


    display_metrics_history(
        history_dataframe
    )


    print()
    print(
        "1_09 metrics module "
        "completed successfully."
    )