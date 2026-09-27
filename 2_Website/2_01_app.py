# ============================================================
# 2_01 - WSN INTERACTIVE WEBSITE
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import sys
import importlib.util
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 2_01_01 - PROJECT PATHS
# ============================================================

CURRENT_FOLDER = Path(__file__).resolve().parent

PROJECT_FOLDER = CURRENT_FOLDER.parent

PYTHON_FOLDER = (
    PROJECT_FOLDER /
    "1_Python"
)


# ============================================================
# 2_01_02 - LOAD SIMULATION MODULE
# ============================================================

def load_module(module_name, file_name):

    file_path = PYTHON_FOLDER / file_name

    spec = importlib.util.spec_from_file_location(
        module_name,
        file_path
    )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


simulation = load_module(
    "simulation",
    "1_10_simulation.py"
)


# ============================================================
# 2_01_03 - PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="ANN-Based LEACH WSN",

    page_icon="📡",

    layout="wide"
)


# ============================================================
# 2_01_04 - TITLE
# ============================================================

st.title(
    "📡 ANN-Based LEACH Wireless Sensor Network"
)

st.markdown(
    """
Interactive simulation of an ANN-assisted
LEACH Wireless Sensor Network.

The simulation performs:

**ANN1 → CH Selection → Clustering → ANN2 →
Main CH Selection → Communication → Energy Update → Metrics**
"""
)


# ============================================================
# 2_01_05 - SIDEBAR
# ============================================================

st.sidebar.header(
    "Simulation Controls"
)


# ============================================================
# NETWORK PARAMETERS
# ============================================================

st.sidebar.subheader(
    "Network"
)

number_of_nodes = st.sidebar.number_input(
    "Number of Nodes",
    min_value=10,
    max_value=1000,
    value=100,
    step=10
)


area_x = st.sidebar.number_input(
    "Area X (m)",
    min_value=10.0,
    max_value=1000.0,
    value=100.0,
    step=10.0
)


area_y = st.sidebar.number_input(
    "Area Y (m)",
    min_value=10.0,
    max_value=1000.0,
    value=100.0,
    step=10.0
)


area_z = st.sidebar.number_input(
    "Area Z (m)",
    min_value=10.0,
    max_value=1000.0,
    value=100.0,
    step=10.0
)


# ============================================================
# ENERGY PARAMETERS
# ============================================================

st.sidebar.subheader(
    "Energy"
)


initial_energy = st.sidebar.number_input(
    "Initial Energy (J)",
    min_value=0.01,
    max_value=100.0,
    value=0.5,
    step=0.1
)


# ============================================================
# BASE STATION PARAMETERS
# ============================================================

st.sidebar.subheader(
    "Base Station"
)


bs_x = st.sidebar.number_input(
    "BS X",
    min_value=-1000.0,
    max_value=2000.0,
    value=50.0,
    step=10.0
)


bs_y = st.sidebar.number_input(
    "BS Y",
    min_value=-1000.0,
    max_value=2000.0,
    value=50.0,
    step=10.0
)


bs_z = st.sidebar.number_input(
    "BS Z",
    min_value=-1000.0,
    max_value=2000.0,
    value=0.0,
    step=10.0
)


# ============================================================
# CLUSTER HEAD PARAMETERS
# ============================================================

st.sidebar.subheader(
    "Clustering"
)


ch_probability = st.sidebar.slider(
    "CH Probability",
    min_value=0.01,
    max_value=0.50,
    value=0.10,
    step=0.01
)


# ============================================================
# RANDOM SEED
# ============================================================

st.sidebar.subheader(
    "Randomization"
)


random_seed = st.sidebar.number_input(
    "Random Seed",
    min_value=0,
    max_value=999999,
    value=42,
    step=1
)


# ============================================================
# PACKET PARAMETERS
# ============================================================

st.sidebar.subheader(
    "Communication"
)


packet_size = st.sidebar.number_input(
    "Packet Size (bits)",
    min_value=100,
    max_value=100000,
    value=4000,
    step=100
)


# ============================================================
# DISPLAY SELECTED PARAMETERS
# ============================================================

with st.sidebar.expander(
    "Selected Parameters"
):

    st.write(
        "Nodes:",
        number_of_nodes
    )

    st.write(
        "Area:",
        f"{area_x} × {area_y} × {area_z} m"
    )

    st.write(
        "Initial Energy:",
        f"{initial_energy} J"
    )

    st.write(
        "Base Station:",
        f"({bs_x}, {bs_y}, {bs_z})"
    )

    st.write(
        "CH Probability:",
        ch_probability
    )

    st.write(
        "Random Seed:",
        random_seed
    )

    st.write(
        "Packet Size:",
        packet_size,
        "bits"
    )


# ============================================================
# 2_01_06 - RUN SIMULATION BUTTON
# ============================================================

run_button = st.sidebar.button(
    "▶ Run Simulation",
    type="primary"
)

# ============================================================
# 2_01_06A - APPLY WEBSITE PARAMETERS
# ============================================================

def apply_parameters():

    # --------------------------------------------------------
    # Main simulation configuration
    # --------------------------------------------------------

    simulation.config.SN = int(
        number_of_nodes
    )

    simulation.config.AREA_X = float(
        area_x
    )

    simulation.config.AREA_Y = float(
        area_y
    )

    simulation.config.AREA_Z = float(
        area_z
    )

    simulation.config.INITIAL_ENERGY = float(
        initial_energy
    )

    simulation.config.BS_X = float(
        bs_x
    )

    simulation.config.BS_Y = float(
        bs_y
    )

    simulation.config.BS_Z = float(
        bs_z
    )

    simulation.config.CH_PROBABILITY = float(
        ch_probability
    )

    simulation.config.RANDOM_SEED = int(
        random_seed
    )


    # --------------------------------------------------------
    # Deployment module
    # --------------------------------------------------------

    simulation.deployment.config.SN = int(
        number_of_nodes
    )

    simulation.deployment.config.AREA_X = float(
        area_x
    )

    simulation.deployment.config.AREA_Y = float(
        area_y
    )

    simulation.deployment.config.AREA_Z = float(
        area_z
    )

    simulation.deployment.config.INITIAL_ENERGY = float(
        initial_energy
    )

    simulation.deployment.config.BS_X = float(
        bs_x
    )

    simulation.deployment.config.BS_Y = float(
        bs_y
    )

    simulation.deployment.config.BS_Z = float(
        bs_z
    )

    simulation.deployment.config.RANDOM_SEED = int(
        random_seed
    )


    # --------------------------------------------------------
    # ANN1 module
    # --------------------------------------------------------

    simulation.ann1.config.SN = int(
        number_of_nodes
    )

    simulation.ann1.config.CH_PROBABILITY = float(
        ch_probability
    )

    simulation.ann1.config.RANDOM_SEED = int(
        random_seed
    )


    # --------------------------------------------------------
    # ANN2 module
    # --------------------------------------------------------

    simulation.ann2.config.RANDOM_SEED = int(
        random_seed
    )


    # --------------------------------------------------------
    # Energy module
    # --------------------------------------------------------

    simulation.communication.energy_model.PACKET_SIZE = int(
        packet_size
    )

# ============================================================
# 2_01_07 - RUN SIMULATION
# ============================================================

if run_button:

    # Apply the values selected in the website
    # to the simulation before starting it.

    apply_parameters()

    with st.spinner(
        "Running WSN simulation..."
    ):

        (

            final_nodes,

            base_station,

            metrics_dataframe,

            round_information_dataframe,

            communication_dataframe,

            final_results

        ) = simulation.run_simulation()


    # ========================================================
    # SAVE RESULTS IN SESSION
    # ========================================================

    st.session_state[
        "final_nodes"
    ] = final_nodes

    st.session_state[
        "base_station"
    ] = base_station

    st.session_state[
        "metrics_dataframe"
    ] = metrics_dataframe

    st.session_state[
        "round_information_dataframe"
    ] = round_information_dataframe

    st.session_state[
        "communication_dataframe"
    ] = communication_dataframe

    st.session_state[
        "final_results"
    ] = final_results


# ============================================================
# 2_01_08 - CHECK WHETHER SIMULATION EXISTS
# ============================================================

if (
    "final_results"
    not in st.session_state
):

    st.info(
        "Set the simulation parameters and press "
        "**Run Simulation** to begin."
    )

    st.stop()


# ============================================================
# 2_01_09 - LOAD STORED RESULTS
# ============================================================

final_nodes = st.session_state[
    "final_nodes"
]

base_station = st.session_state[
    "base_station"
]

metrics_dataframe = st.session_state[
    "metrics_dataframe"
]

round_information_dataframe = (
    st.session_state[
        "round_information_dataframe"
    ]
)

communication_dataframe = (
    st.session_state[
        "communication_dataframe"
    ]
)

final_results = st.session_state[
    "final_results"
]


# ============================================================
# 2_01_10 - SUMMARY
# ============================================================

st.header(
    "Simulation Summary"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Rounds",
        final_results[
            "TotalRounds"
        ]
    )


with col2:

    st.metric(
        "FND",
        final_results[
            "FND"
        ]
    )


with col3:

    st.metric(
        "HND",
        final_results[
            "HND"
        ]
    )


with col4:

    st.metric(
        "LND",
        final_results[
            "LND"
        ]
    )


# ============================================================
# 2_01_11 - ENERGY / THROUGHPUT
# ============================================================

st.header(
    "Energy and Throughput"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Energy Consumed",
        f'{final_results["TotalEnergyConsumed"]:.6f} J'
    )


with col2:

    st.metric(
        "Throughput",
        f'{final_results["TotalThroughputBits"]:,} bits'
    )


with col3:

    st.metric(
        "Final Residual Energy",
        f'{final_results["FinalResidualEnergy"]:.6f} J'
    )


# ============================================================
# 2_01_12 - ALIVE NODES GRAPH
# ============================================================

st.header(
    "Network Lifetime"
)


if not metrics_dataframe.empty:

    fig, ax = plt.subplots()

    ax.plot(
        metrics_dataframe["Round"],
        metrics_dataframe["AliveNodes"]
    )

    ax.set_xlabel(
        "Round"
    )

    ax.set_ylabel(
        "Alive Nodes"
    )

    ax.set_title(
        "Alive Nodes vs Round"
    )

    ax.grid(
        True
    )

    st.pyplot(
        fig
    )


# ============================================================
# 2_01_13 - RESIDUAL ENERGY GRAPH
# ============================================================

st.header(
    "Residual Energy"
)


if not metrics_dataframe.empty:

    fig, ax = plt.subplots()

    ax.plot(
        metrics_dataframe["Round"],
        metrics_dataframe["ResidualEnergy"]
    )

    ax.set_xlabel(
        "Round"
    )

    ax.set_ylabel(
        "Residual Energy (J)"
    )

    ax.set_title(
        "Residual Energy vs Round"
    )

    ax.grid(
        True
    )

    st.pyplot(
        fig
    )


# ============================================================
# 2_01_14 - ENERGY CONSUMPTION GRAPH
# ============================================================

st.header(
    "Energy Consumption"
)


if not metrics_dataframe.empty:

    fig, ax = plt.subplots()

    ax.plot(
        metrics_dataframe["Round"],
        metrics_dataframe["EnergyConsumed"]
    )

    ax.set_xlabel(
        "Round"
    )

    ax.set_ylabel(
        "Energy Consumed (J)"
    )

    ax.set_title(
        "Energy Consumption per Round"
    )

    ax.grid(
        True
    )

    st.pyplot(
        fig
    )


# ============================================================
# 2_01_15 - THROUGHPUT GRAPH
# ============================================================

st.header(
    "Throughput"
)


if not metrics_dataframe.empty:

    cumulative_throughput = (
        metrics_dataframe[
            "ThroughputBits"
        ].cumsum()
    )

    fig, ax = plt.subplots()

    ax.plot(
        metrics_dataframe["Round"],
        cumulative_throughput
    )

    ax.set_xlabel(
        "Round"
    )

    ax.set_ylabel(
        "Cumulative Throughput (bits)"
    )

    ax.set_title(
        "Cumulative Throughput"
    )

    ax.grid(
        True
    )

    st.pyplot(
        fig
    )


# ============================================================
# 2_01_16 - CH HISTORY
# ============================================================

st.header(
    "CH / Main CH Selection History"
)


st.dataframe(
    round_information_dataframe,

    use_container_width=True
)


# ============================================================
# 2_01_17 - METRICS TABLE
# ============================================================

st.header(
    "Round-by-Round Metrics"
)


st.dataframe(
    metrics_dataframe,

    use_container_width=True
)


# ============================================================
# 2_01_18 - COMMUNICATION HISTORY
# ============================================================

st.header(
    "Communication History"
)


st.dataframe(
    communication_dataframe,

    use_container_width=True
)


# ============================================================
# 2_01_19 - FINAL NODE INFORMATION
# ============================================================

st.header(
    "Final Node Status"
)


st.dataframe(
    final_nodes,

    use_container_width=True
)


# ============================================================
# 2_01_20 - DOWNLOAD RESULTS
# ============================================================

st.header(
    "Download Results"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.download_button(

        label="Download Metrics CSV",

        data=metrics_dataframe.to_csv(
            index=False
        ),

        file_name="round_metrics.csv",

        mime="text/csv"
    )


with col2:

    st.download_button(

        label="Download CH History",

        data=round_information_dataframe.to_csv(
            index=False
        ),

        file_name="ch_main_ch_history.csv",

        mime="text/csv"
    )


with col3:

    st.download_button(

        label="Download Communication",

        data=communication_dataframe.to_csv(
            index=False
        ),

        file_name="communication_history.csv",

        mime="text/csv"
    )