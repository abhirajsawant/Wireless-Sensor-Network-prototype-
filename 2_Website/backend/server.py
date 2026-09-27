# ============================================================
# WSN WEBSITE BACKEND
# Flask API
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS

import importlib.util
from pathlib import Path
import traceback


# ============================================================
# 5_01 - PATHS
# ============================================================

CURRENT_FOLDER = Path(__file__).resolve().parent

WEBSITE_FOLDER = CURRENT_FOLDER.parent

PROJECT_FOLDER = WEBSITE_FOLDER.parent

PYTHON_FOLDER = PROJECT_FOLDER / "1_Python"


# ============================================================
# 5_02 - FLASK APPLICATION
# ============================================================

app = Flask(__name__)

CORS(app)


# ============================================================
# 5_03 - LOAD PYTHON MODULE
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
# 5_04 - HEALTH CHECK
# ============================================================

@app.route(
    "/api/health",
    methods=["GET"]
)
def health_check():

    return jsonify({

        "status": "ok",

        "message":
            "WSN Python backend is running."

    })


# ============================================================
# 5_05 - RUN SIMULATION
# ============================================================

@app.route(
    "/api/run-simulation",
    methods=["POST"]
)
def run_simulation():

    try:

        # ----------------------------------------------------
        # Receive JSON from JavaScript
        # ----------------------------------------------------

        data = request.get_json()

        if data is None:

            return jsonify({

                "success": False,

                "error":
                    "No JSON data received."

            }), 400


        # ----------------------------------------------------
        # Read parameters
        # ----------------------------------------------------

        number_of_nodes = int(
            data.get(
                "numberOfNodes",
                100
            )
        )

        initial_energy = float(
            data.get(
                "initialEnergy",
                0.5
            )
        )

        ch_probability = float(
            data.get(
                "chProbability",
                0.10
            )
        )

        packet_size = int(
            data.get(
                "packetSize",
                4000
            )
        )

        area_x = float(
            data.get(
                "areaX",
                100
            )
        )

        area_y = float(
            data.get(
                "areaY",
                100
            )
        )

        area_z = float(
            data.get(
                "areaZ",
                100
            )
        )

        bs_x = float(
            data.get(
                "bsX",
                50
            )
        )

        bs_y = float(
            data.get(
                "bsY",
                50
            )
        )

        bs_z = float(
            data.get(
                "bsZ",
                0
            )
        )


        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        if number_of_nodes < 10:

            return jsonify({

                "success": False,

                "error":
                    "Number of nodes must be at least 10."

            }), 400


        if initial_energy <= 0:

            return jsonify({

                "success": False,

                "error":
                    "Initial energy must be greater than 0."

            }), 400


        if not 0 < ch_probability <= 0.50:

            return jsonify({

                "success": False,

                "error":
                    "CH probability must be between 0.01 and 0.50."

            }), 400


        if packet_size <= 0:

            return jsonify({

                "success": False,

                "error":
                    "Packet size must be greater than 0."

            }), 400


        if (
            area_x <= 0
            or area_y <= 0
            or area_z <= 0
        ):

            return jsonify({

                "success": False,

                "error":
                    "Network dimensions must be greater than 0."

            }), 400


        # ====================================================
        # APPLY PARAMETERS
        # ====================================================

        simulation.config.SN = (
            number_of_nodes
        )

        simulation.config.AREA_X = (
            area_x
        )

        simulation.config.AREA_Y = (
            area_y
        )

        simulation.config.AREA_Z = (
            area_z
        )

        simulation.config.INITIAL_ENERGY = (
            initial_energy
        )

        simulation.config.BS_X = (
            bs_x
        )

        simulation.config.BS_Y = (
            bs_y
        )

        simulation.config.BS_Z = (
            bs_z
        )

        simulation.config.CH_PROBABILITY = (
            ch_probability
        )


        # ====================================================
        # RUN EXISTING SIMULATION
        # ====================================================

        (

            final_nodes,

            base_station,

            metrics_dataframe,

            round_information_dataframe,

            communication_dataframe,

            final_results

        ) = simulation.run_simulation()


        # ====================================================
        # CONVERT RESULTS TO JSON
        # ====================================================

        metrics = (
            metrics_dataframe
            .fillna(0)
            .to_dict(
                orient="records"
            )
        )


        ch_history = (
            round_information_dataframe
            .fillna("")
            .to_dict(
                orient="records"
            )
        )


        communication_history = (
            communication_dataframe
            .fillna("")
            .to_dict(
                orient="records"
            )
        )


        nodes = (
            final_nodes
            .fillna("")
            .to_dict(
                orient="records"
            )
        )


        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "success": True,

            "message":
                "Simulation completed successfully.",

            "parameters": {

                "numberOfNodes":
                    number_of_nodes,

                "initialEnergy":
                    initial_energy,

                "chProbability":
                    ch_probability,

                "packetSize":
                    packet_size,

                "areaX":
                    area_x,

                "areaY":
                    area_y,

                "areaZ":
                    area_z,

                "bsX":
                    bs_x,

                "bsY":
                    bs_y,

                "bsZ":
                    bs_z

            },

            "baseStation":
                base_station,

            "finalResults":
                final_results,

            "metrics":
                metrics,

            "chHistory":
                ch_history,

            "communicationHistory":
                communication_history,

            "nodes":
                nodes

        })


    except Exception as error:

        print(
            "\n========== SIMULATION ERROR =========="
        )

        traceback.print_exc()

        print(
            "======================================\n"
        )


        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# ============================================================
# 5_06 - START SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print(" ANN-BASED LEACH WSN BACKEND")
    print("==============================================")
    print()
    print(
        "Server running at:"
    )
    print(
        "http://127.0.0.1:5000"
    )
    print()
    print(
        "Health check:"
    )
    print(
        "http://127.0.0.1:5000/api/health"
    )
    print()
    print("==============================================")
    print()


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )
    