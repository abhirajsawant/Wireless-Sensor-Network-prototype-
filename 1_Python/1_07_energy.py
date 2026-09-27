# ============================================================
# 1_07 - ENERGY MODEL
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import numpy as np
import importlib.util
from pathlib import Path


# ============================================================
# 1_07_01 - LOAD CONFIGURATION
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
# 1_07_02 - RADIO ENERGY PARAMETERS
# ============================================================

# Energy required by the electronics to process
# one bit of data.
#
# Unit:
# Joule / bit

E_ELEC = 50e-9


# Amplifier energy for free-space propagation.
#
# Unit:
# Joule / bit / m^2

E_FS = 10e-12


# Amplifier energy for multipath propagation.
#
# Unit:
# Joule / bit / m^4

E_MP = 0.0013e-12


# Data aggregation energy.
#
# Unit:
# Joule / bit

E_DA = 5e-9


# Packet size.
#
# Unit:
# bits

PACKET_SIZE = 4000


# ============================================================
# 1_07_03 - DISTANCE THRESHOLD
# ============================================================

def calculate_d0():

    """
    Calculate the crossover distance between
    free-space and multipath propagation models.

    d0 = sqrt(E_FS / E_MP)
    """

    d0 = np.sqrt(
        E_FS / E_MP
    )

    return d0


# ============================================================
# 1_07_04 - TRANSMISSION ENERGY
# ============================================================

def transmission_energy(
    bits,
    distance
):

    """
    Calculate energy required to transmit data.

    First-order radio model:

        E_TX(k,d) = E_ELEC*k + E_AMP*k*d^n

    Free-space model is used when:

        d < d0

    Multipath model is used when:

        d >= d0
    """

    distance = max(
        float(distance),
        0.0
    )


    if distance < calculate_d0():

        # ----------------------------------------------------
        # Free-space model
        # ----------------------------------------------------

        energy = (

            E_ELEC * bits

            +

            E_FS
            * bits
            * distance**2

        )

    else:

        # ----------------------------------------------------
        # Multipath model
        # ----------------------------------------------------

        energy = (

            E_ELEC * bits

            +

            E_MP
            * bits
            * distance**4

        )


    return energy


# ============================================================
# 1_07_05 - RECEPTION ENERGY
# ============================================================

def reception_energy(
    bits
):

    """
    Calculate energy required for a node to receive
    a packet.

        E_RX(k) = E_ELEC * k
    """

    energy = (
        E_ELEC * bits
    )

    return energy


# ============================================================
# 1_07_06 - DATA AGGREGATION ENERGY
# ============================================================

def aggregation_energy(
    bits
):

    """
    Calculate energy required for data aggregation.

        E_DA(k) = E_DA * k
    """

    energy = (
        E_DA * bits
    )

    return energy


# ============================================================
# 1_07_07 - COMPLETE CH RECEIVE + AGGREGATION ENERGY
# ============================================================

def ch_receive_aggregation_energy(
    number_of_packets,
    bits
):

    """
    Calculate the energy consumed by a CH when it:

        1. Receives packets from member nodes.
        2. Performs data aggregation.

    Parameters
    ----------
    number_of_packets : int
        Number of received packets.

    bits : int
        Bits per packet.
    """

    receive_energy = (

        number_of_packets

        *

        reception_energy(
            bits
        )

    )


    aggregation = (

        number_of_packets

        *

        aggregation_energy(
            bits
        )

    )


    total_energy = (
        receive_energy
        +
        aggregation
    )


    return total_energy


# ============================================================
# 1_07_08 - SUBTRACT ENERGY FROM NODE
# ============================================================

def consume_energy(
    current_energy,
    consumed_energy
):

    """
    Subtract consumed energy from current residual energy.

    Energy is never allowed to become negative.
    """

    current_energy = max(
        float(current_energy),
        0.0
    )

    consumed_energy = max(
        float(consumed_energy),
        0.0
    )


    remaining_energy = (

        current_energy
        -
        consumed_energy

    )


    remaining_energy = max(
        remaining_energy,
        0.0
    )


    return remaining_energy


# ============================================================
# 1_07_09 - CHECK NODE ALIVE STATUS
# ============================================================

def is_node_alive(
    energy
):

    """
    Determine whether a node is still alive.

    A node is alive when residual energy > 0.
    """

    return (
        energy > 0
    )


# ============================================================
# 1_07_10 - UPDATE NODE ENERGY
# ============================================================

def update_node_energy(
    nodes,
    node_index,
    consumed_energy
):

    """
    Subtract energy from a specific node and update
    its Alive status.
    """

    nodes = nodes.copy()


    current_energy = nodes.loc[
        node_index,
        "energy"
    ]


    new_energy = consume_energy(

        current_energy,

        consumed_energy

    )


    nodes.loc[
        node_index,
        "energy"
    ] = new_energy


    # --------------------------------------------------------
    # Create Alive column if it does not exist
    # --------------------------------------------------------

    if "Alive" not in nodes.columns:

        nodes["Alive"] = (
            nodes["energy"] > 0
        )


    # --------------------------------------------------------
    # Update status
    # --------------------------------------------------------

    nodes.loc[
        node_index,
        "Alive"
    ] = is_node_alive(
        new_energy
    )


    return nodes


# ============================================================
# 1_07_11 - UPDATE ALL NODE ENERGY STATUS
# ============================================================

def update_alive_status(
    nodes
):

    """
    Update Alive status for every node.
    """

    nodes = nodes.copy()


    nodes["Alive"] = (
        nodes["energy"] > 0
    )


    return nodes


# ============================================================
# 1_07_12 - ENERGY SUMMARY
# ============================================================

def calculate_energy_summary(
    nodes
):

    """
    Calculate basic network energy statistics.
    """

    total_energy = (
        nodes["energy"].sum()
    )


    alive_nodes = int(
        np.sum(
            nodes["energy"] > 0
        )
    )


    dead_nodes = (
        len(nodes)
        -
        alive_nodes
    )


    average_energy = (

        total_energy / len(nodes)

        if len(nodes) > 0

        else 0.0

    )


    return {

        "total_energy":
            total_energy,

        "average_energy":
            average_energy,

        "alive_nodes":
            alive_nodes,

        "dead_nodes":
            dead_nodes

    }


# ============================================================
# 1_07_13 - DISPLAY ENERGY MODEL
# ============================================================

def display_energy_model():

    """
    Display the configured radio-energy model.
    """

    print()
    print("==============================================")
    print(" 1_07 - ENERGY MODEL")
    print("==============================================")

    print(
        "E_ELEC              :",
        E_ELEC,
        "J/bit"
    )

    print(
        "E_FS                :",
        E_FS,
        "J/bit/m^2"
    )

    print(
        "E_MP                :",
        E_MP,
        "J/bit/m^4"
    )

    print(
        "E_DA                :",
        E_DA,
        "J/bit"
    )

    print(
        "Packet size         :",
        PACKET_SIZE,
        "bits"
    )

    print(
        "Crossover distance  :",
        round(
            calculate_d0(),
            3
        ),
        "m"
    )

    print("----------------------------------------------")


# ============================================================
# 1_07_14 - MODULE TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Display model
    # --------------------------------------------------------

    display_energy_model()


    # ========================================================
    # Test transmission
    # ========================================================

    test_distance = 50

    tx_energy = transmission_energy(

        PACKET_SIZE,

        test_distance

    )


    print(
        "TX energy at",
        test_distance,
        "m       :",
        tx_energy,
        "J"
    )


    # ========================================================
    # Test reception
    # ========================================================

    rx_energy = reception_energy(
        PACKET_SIZE
    )


    print(
        "RX energy per packet     :",
        rx_energy,
        "J"
    )


    # ========================================================
    # Test aggregation
    # ========================================================

    aggregation = aggregation_energy(
        PACKET_SIZE
    )


    print(
        "Aggregation energy       :",
        aggregation,
        "J"
    )


    # ========================================================
    # Test CH receive + aggregation
    # ========================================================

    number_of_packets = 5

    ch_energy = (
        ch_receive_aggregation_energy(

            number_of_packets,

            PACKET_SIZE

        )
    )


    print(
        "CH RX + aggregation",
        f"({number_of_packets} packets):",
        ch_energy,
        "J"
    )


    # ========================================================
    # Test energy subtraction
    # ========================================================

    initial_energy = 0.5

    consumed = 0.01

    remaining = consume_energy(

        initial_energy,

        consumed

    )


    print(
        "Energy after consumption :",
        remaining,
        "J"
    )


    # ========================================================
    # Test node death
    # ========================================================

    remaining_after_death = consume_energy(

        0.005,

        0.01

    )


    print(
        "Energy after overuse     :",
        remaining_after_death,
        "J"
    )


    print("----------------------------------------------")

    print(
        "Energy model completed successfully."
    )