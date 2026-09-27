# ============================================================
# 1_10 - WSN SIMULATION ENGINE
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import numpy as np
import pandas as pd
import importlib.util
from pathlib import Path


# ============================================================
# 1_10_01 - LOAD MODULES
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

communication = load_module(
    "communication",
    "1_08_communication.py"
)

metrics = load_module(
    "metrics",
    "1_09_metrics.py"
)


# ============================================================
# 1_10_02 - SIMULATION SETTINGS
# ============================================================

# This is NOT the network lifetime.
#
# It is only a protection against an accidental infinite
# loop caused by a programming error.
#
# The actual simulation stops when all nodes are dead.

SAFETY_MAX_ROUNDS = 100000


# ============================================================
# 1_10_03 - ALIVE NODE COUNT
# ============================================================

def count_alive_nodes(nodes):

    return int(
        np.sum(
            nodes["energy"] > 0
        )
    )


# ============================================================
# 1_10_04 - DEAD NODE COUNT
# ============================================================

def count_dead_nodes(nodes):

    return int(
        np.sum(
            nodes["energy"] <= 0
        )
    )


# ============================================================
# 1_10_05 - GET CH NODE IDs
# ============================================================

def get_cluster_head_ids(
    nodes,
    ch_indices
):

    ch_ids = []

    for index in ch_indices:

        if index in nodes.index:

            ch_ids.append(
                int(
                    nodes.loc[
                        index,
                        "NodeID"
                    ]
                )
            )

    return ch_ids


# ============================================================
# 1_10_06 - GET MAIN CH ID
# ============================================================

def get_main_ch_id(
    main_ch_id
):

    if main_ch_id is None:

        return None

    try:

        return int(main_ch_id)

    except (TypeError, ValueError):

        return main_ch_id


# ============================================================
# 1_10_07 - RUN ANN1
# ============================================================

def run_ann1(
    nodes
):

    result = (
        ann1.run_ann1_ch_selection(
            nodes
        )
    )

    # The existing ANN1 module returns more than
    # the three values needed here.
    #
    # We intentionally use only the required values.

    updated_nodes = result[0]

    ch_indices = result[1]

    ann1_model = result[2]

    return (
        updated_nodes,
        ch_indices,
        ann1_model
    )


# ============================================================
# 1_10_08 - RUN CLUSTERING
# ============================================================

def run_clustering(
    nodes,
    ch_indices
):

    result = (
        clustering.create_clusters(
            nodes,
            ch_indices
        )
    )

    # Existing clustering module returns four values.
    # The simulation needs the first two.

    updated_nodes = result[0]

    clusters = result[1]

    return (
        updated_nodes,
        clusters
    )


# ============================================================
# 1_10_09 - RUN ANN2
# ============================================================

def run_ann2(
    nodes,
    ch_indices
):

    result = (
        ann2.run_ann2_main_ch_selection(
            nodes,
            ch_indices
        )
    )

    # Existing ANN2 module may return additional
    # information. We use the first three values.

    updated_nodes = result[0]

    main_ch_id = result[1]

    ann2_model = result[2]

    return (
        updated_nodes,
        main_ch_id,
        ann2_model
    )


# ============================================================
# 1_10_10 - RUN ONE COMPLETE ROUND
# ============================================================

def run_one_round(
    round_number,
    nodes,
    base_station,
    current_fnd,
    current_hnd,
    current_lnd
):

    # ========================================================
    # Save energy before communication
    # ========================================================

    previous_nodes = nodes.copy()


    # ========================================================
    # STEP 1 - ANN1
    # ========================================================

    nodes, ch_indices, ann1_model = (
        run_ann1(nodes)
    )


    # ========================================================
    # STEP 2 - CLUSTERING
    # ========================================================

    nodes, clusters = (
        run_clustering(
            nodes,
            ch_indices
        )
    )


    # ========================================================
    # STEP 3 - ANN2
    # ========================================================

    nodes, main_ch_id, ann2_model = (
        run_ann2(
            nodes,
            ch_indices
        )
    )


    # ========================================================
    # STEP 4 - CHECK MAIN CH
    # ========================================================

    main_ch_id = get_main_ch_id(
        main_ch_id
    )


    # ========================================================
    # STEP 5 - COMMUNICATION
    # ========================================================

    nodes, communication_table = (
        communication.run_communication_round(

            nodes,

            base_station,

            main_ch_id
        )
    )


    # ========================================================
    # STEP 6 - METRICS
    # ========================================================

    round_metrics, current_fnd, current_hnd, current_lnd = (

        metrics.calculate_round_metrics(

            round_number,

            previous_nodes,

            nodes,

            communication_table,

            current_fnd,

            current_hnd,

            current_lnd
        )
    )


    # ========================================================
    # STEP 7 - ROUND INFORMATION
    # ========================================================

    round_information = {

        "Round":
            round_number,

        "CH_IDs":
            get_cluster_head_ids(
                nodes,
                ch_indices
            ),

        "Main_CH":
            main_ch_id,

        "Number_of_CHs":
            len(ch_indices),

        "AliveNodes":
            count_alive_nodes(
                nodes
            ),

        "DeadNodes":
            count_dead_nodes(
                nodes
            ),

        "ResidualEnergy":
            float(
                nodes["energy"].sum()
            ),

        "CommunicationRecords":
            len(
                communication_table
            )
    }


    return (

        nodes,

        round_metrics,

        round_information,

        communication_table,

        current_fnd,

        current_hnd,

        current_lnd
    )


# ============================================================
# 1_10_11 - RUN COMPLETE SIMULATION
# ============================================================

def run_simulation():

    print()
    print("================================================")
    print(" ANN-BASED LEACH WSN SIMULATION")
    print("================================================")


    # ========================================================
    # INITIAL DEPLOYMENT
    # ========================================================

    nodes, base_station = (
        deployment.deploy_network()
    )


    print()
    print(
        "Initial deployment completed."
    )

    print(
        "Total nodes :",
        len(nodes)
    )

    print(
        "Initial energy :",
        round(
            nodes["energy"].sum(),
            6
        ),
        "J"
    )


    # ========================================================
    # INITIAL METRIC VARIABLES
    # ========================================================

    round_metrics_history = []

    round_information_history = []

    communication_history = []

    fnd = None

    hnd = None

    lnd = None

    round_number = 0


    # ========================================================
    # MAIN SIMULATION LOOP
    # ========================================================

    while (
        count_alive_nodes(nodes) > 0
        and round_number < SAFETY_MAX_ROUNDS
    ):

        round_number += 1


        # ----------------------------------------------------
        # Execute one complete WSN round
        # ----------------------------------------------------

        (

            nodes,

            round_metrics,

            round_information,

            communication_table,

            fnd,

            hnd,

            lnd

        ) = run_one_round(

            round_number,

            nodes,

            base_station,

            fnd,

            hnd,

            lnd
        )


        # ----------------------------------------------------
        # Store metrics
        # ----------------------------------------------------

        round_metrics_history.append(
            round_metrics
        )


        # ----------------------------------------------------
        # Store CH / Main CH information
        # ----------------------------------------------------

        round_information_history.append(
            round_information
        )


        # ----------------------------------------------------
        # Store communication records
        # ----------------------------------------------------

        if not communication_table.empty:

            communication_table = (
                communication_table.copy()
            )

            communication_table[
                "Round"
            ] = round_number

            communication_history.append(
                communication_table
            )


        # ----------------------------------------------------
        # Display current round
        # ----------------------------------------------------

        print(
            "Round",
            round_number,
            "| CHs:",
            round_information["CH_IDs"],
            "| Main CH:",
            round_information["Main_CH"],
            "| Alive:",
            round_information["AliveNodes"],
            "| Energy:",
            round(
                round_information[
                    "ResidualEnergy"
                ],
                6
            ),
            "J"
        )


        # ----------------------------------------------------
        # Stop when all nodes are dead
        # ----------------------------------------------------

        if count_alive_nodes(nodes) == 0:

            lnd = round_number

            break


    # ========================================================
    # CREATE METRICS DATAFRAME
    # ========================================================

    metrics_dataframe = (
        metrics.history_to_dataframe(
            round_metrics_history
        )
    )


    # ========================================================
    # CREATE ROUND INFORMATION DATAFRAME
    # ========================================================

    round_information_dataframe = (
        pd.DataFrame(
            round_information_history
        )
    )


    # ========================================================
    # CREATE COMMUNICATION DATAFRAME
    # ========================================================

    if communication_history:

        communication_dataframe = (
            pd.concat(
                communication_history,
                ignore_index=True
            )
        )

    else:

        communication_dataframe = (
            pd.DataFrame()
        )


    # ========================================================
    # FINAL SIMULATION RESULTS
    # ========================================================

    total_energy_consumed = (

        float(
            metrics_dataframe[
                "EnergyConsumed"
            ].sum()
        )

        if not metrics_dataframe.empty

        else 0.0
    )


    total_throughput = (

        int(
            metrics_dataframe[
                "ThroughputBits"
            ].sum()
        )

        if not metrics_dataframe.empty

        else 0
    )


    total_node_to_ch_packets = (

        int(
            metrics_dataframe[
                "NodeToCHPackets"
            ].sum()
        )

        if not metrics_dataframe.empty

        else 0
    )


    total_ch_to_main_packets = (

        int(
            metrics_dataframe[
                "CHToMainCHPackets"
            ].sum()
        )

        if not metrics_dataframe.empty

        else 0
    )


    total_main_ch_to_bs_packets = (

        int(
            metrics_dataframe[
                "MainCHToBSPackets"
            ].sum()
        )

        if not metrics_dataframe.empty

        else 0
    )


    # ========================================================
    # FINAL RESULT DICTIONARY
    # ========================================================

    final_results = {

        "TotalRounds":
            round_number,

        "FND":
            fnd,

        "HND":
            hnd,

        "LND":
            lnd,

        "TotalEnergyConsumed":
            total_energy_consumed,

        "TotalThroughputBits":
            total_throughput,

        "TotalNodeToCHPackets":
            total_node_to_ch_packets,

        "TotalCHToMainCHPackets":
            total_ch_to_main_packets,

        "TotalMainCHToBSPackets":
            total_main_ch_to_bs_packets,

        "FinalAliveNodes":
            count_alive_nodes(nodes),

        "FinalDeadNodes":
            count_dead_nodes(nodes),

        "FinalResidualEnergy":
            float(
                nodes["energy"].sum()
            )
    }


    return (

        nodes,

        base_station,

        metrics_dataframe,

        round_information_dataframe,

        communication_dataframe,

        final_results
    )


# ============================================================
# 1_10_12 - DISPLAY FINAL RESULTS
# ============================================================

def display_final_results(
    final_results
):

    print()
    print("================================================")
    print(" FINAL SIMULATION RESULTS")
    print("================================================")

    print(
        "Total rounds              :",
        final_results["TotalRounds"]
    )

    print(
        "FND                       :",
        final_results["FND"]
    )

    print(
        "HND                       :",
        final_results["HND"]
    )

    print(
        "LND                       :",
        final_results["LND"]
    )

    print(
        "Total energy consumed     :",
        round(
            final_results[
                "TotalEnergyConsumed"
            ],
            6
        ),
        "J"
    )

    print(
        "Total throughput          :",
        final_results[
            "TotalThroughputBits"
        ],
        "bits"
    )

    print(
        "Node -> CH packets       :",
        final_results[
            "TotalNodeToCHPackets"
        ]
    )

    print(
        "CH -> Main CH packets    :",
        final_results[
            "TotalCHToMainCHPackets"
        ]
    )

    print(
        "Main CH -> BS packets    :",
        final_results[
            "TotalMainCHToBSPackets"
        ]
    )

    print(
        "Final alive nodes         :",
        final_results[
            "FinalAliveNodes"
        ]
    )

    print(
        "Final dead nodes          :",
        final_results[
            "FinalDeadNodes"
        ]
    )

    print(
        "Final residual energy     :",
        round(
            final_results[
                "FinalResidualEnergy"
            ],
            6
        ),
        "J"
    )

    print("================================================")


# ============================================================
# 1_10_13 - DISPLAY CH HISTORY
# ============================================================

def display_ch_history(
    round_information_dataframe
):

    if round_information_dataframe.empty:

        print(
            "No CH history available."
        )

        return


    print()
    print("================================================")
    print(" CH / MAIN CH HISTORY")
    print("================================================")


    for _, row in (
        round_information_dataframe.iterrows()
    ):

        print(
            "Round",
            int(row["Round"]),
            "| CHs:",
            row["CH_IDs"],
            "| Main CH:",
            row["Main_CH"]
        )


# ============================================================
# 1_10_14 - MODULE TEST
# ============================================================

if __name__ == "__main__":

    (

        final_nodes,

        base_station,

        metrics_dataframe,

        round_information_dataframe,

        communication_dataframe,

        final_results

    ) = run_simulation()


    # --------------------------------------------------------
    # Display final results
    # --------------------------------------------------------

    display_final_results(
        final_results
    )


    # --------------------------------------------------------
    # Display CH selection history
    # --------------------------------------------------------

    display_ch_history(
        round_information_dataframe
    )


    # --------------------------------------------------------
    # Display metrics table
    # --------------------------------------------------------

    print()
    print("================================================")
    print(" ROUND METRICS TABLE")
    print("================================================")

    if not metrics_dataframe.empty:

        print(
            metrics_dataframe.to_string(
                index=False
            )
        )

    else:

        print(
            "No metrics were generated."
        )


    # --------------------------------------------------------
    # Display communication record count
    # --------------------------------------------------------

    print()
    print(
        "Total communication records :",
        len(
            communication_dataframe
        )
    )


    print()
    print(
        "1_10 simulation module "
        "completed successfully."
    )