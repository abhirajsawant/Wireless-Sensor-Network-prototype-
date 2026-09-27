# ============================================================
# 1_11 - MAIN PROGRAM
# ANN-BASED LEACH WIRELESS SENSOR NETWORK
# ============================================================

import importlib.util
from pathlib import Path


# ============================================================
# 1_11_01 - LOAD SIMULATION MODULE
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


simulation = load_module(
    "simulation",
    "1_10_simulation.py"
)


# ============================================================
# 1_11_02 - RESULTS FOLDER
# ============================================================

PROJECT_FOLDER = CURRENT_FOLDER.parent

RESULTS_FOLDER = (
    PROJECT_FOLDER /
    "3_Results"
)


def create_results_folder():

    RESULTS_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# 1_11_03 - SAVE RESULTS
# ============================================================

def save_results(
    metrics_dataframe,
    round_information_dataframe,
    communication_dataframe
):

    create_results_folder()


    # --------------------------------------------------------
    # Save round metrics
    # --------------------------------------------------------

    metrics_path = (
        RESULTS_FOLDER /
        "round_metrics.csv"
    )

    metrics_dataframe.to_csv(
        metrics_path,
        index=False
    )


    # --------------------------------------------------------
    # Save CH / Main CH history
    # --------------------------------------------------------

    ch_history_path = (
        RESULTS_FOLDER /
        "ch_main_ch_history.csv"
    )

    round_information_dataframe.to_csv(
        ch_history_path,
        index=False
    )


    # --------------------------------------------------------
    # Save communication records
    # --------------------------------------------------------

    communication_path = (
        RESULTS_FOLDER /
        "communication_history.csv"
    )

    communication_dataframe.to_csv(
        communication_path,
        index=False
    )


    print()
    print("================================================")
    print(" RESULTS SAVED")
    print("================================================")

    print(
        "Round metrics          :",
        metrics_path
    )

    print(
        "CH/Main CH history     :",
        ch_history_path
    )

    print(
        "Communication history  :",
        communication_path
    )


# ============================================================
# 1_11_04 - MAIN PROGRAM
# ============================================================

def main():

    print()
    print("================================================")
    print(" ANN-BASED LEACH WSN")
    print(" MAIN PROGRAM")
    print("================================================")

    print()
    print(
        "Starting complete WSN simulation..."
    )

    print()


    # ========================================================
    # RUN COMPLETE SIMULATION
    # ========================================================

    (

        final_nodes,

        base_station,

        metrics_dataframe,

        round_information_dataframe,

        communication_dataframe,

        final_results

    ) = simulation.run_simulation()


    # ========================================================
    # DISPLAY FINAL RESULTS
    # ========================================================

    simulation.display_final_results(
        final_results
    )


    # ========================================================
    # DISPLAY CH / MAIN CH HISTORY
    # ========================================================

    simulation.display_ch_history(
        round_information_dataframe
    )


    # ========================================================
    # DISPLAY RESULTS SUMMARY
    # ========================================================

    print()
    print("================================================")
    print(" RESULTS SUMMARY")
    print("================================================")

    print(
        "Rounds simulated        :",
        final_results["TotalRounds"]
    )

    print(
        "First Node Death (FND)  :",
        final_results["FND"]
    )

    print(
        "Half Node Death (HND)   :",
        final_results["HND"]
    )

    print(
        "Last Node Death (LND)   :",
        final_results["LND"]
    )

    print(
        "Total energy consumed   :",
        round(
            final_results[
                "TotalEnergyConsumed"
            ],
            6
        ),
        "J"
    )

    print(
        "Total throughput        :",
        final_results[
            "TotalThroughputBits"
        ],
        "bits"
    )

    print(
        "Final alive nodes       :",
        final_results[
            "FinalAliveNodes"
        ]
    )

    print(
        "Final dead nodes        :",
        final_results[
            "FinalDeadNodes"
        ]
    )

    print(
        "Final residual energy   :",
        round(
            final_results[
                "FinalResidualEnergy"
            ],
            6
        ),
        "J"
    )


    # ========================================================
    # SAVE CSV RESULTS
    # ========================================================

    save_results(

        metrics_dataframe,

        round_information_dataframe,

        communication_dataframe
    )


    # ========================================================
    # FINISHED
    # ========================================================

    print()
    print("================================================")
    print(" COMPLETE SIMULATION FINISHED")
    print("================================================")


# ============================================================
# 1_11_05 - PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()