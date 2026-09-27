// ============================================================
// 6_01 - ANN-BASED LEACH WSN WEBSITE
// Frontend JavaScript
// ============================================================


// ============================================================
// 6_02 - BACKEND URL
// ============================================================

const BACKEND_URL =
    "http://127.0.0.1:5000";


// ============================================================
// 6_03 - GET FORM ELEMENTS
// ============================================================

const nodeCountInput =
    document.getElementById("nodeCount");

const initialEnergyInput =
    document.getElementById("initialEnergy");

const chProbabilityInput =
    document.getElementById("chProbability");

const packetSizeInput =
    document.getElementById("packetSize");

const areaXInput =
    document.getElementById("areaX");

const areaYInput =
    document.getElementById("areaY");

const areaZInput =
    document.getElementById("areaZ");

const bsXInput =
    document.getElementById("bsX");

const bsYInput =
    document.getElementById("bsY");

const bsZInput =
    document.getElementById("bsZ");


// ============================================================
// 6_04 - GET DASHBOARD ELEMENTS
// ============================================================

const runSimulationButton =
    document.getElementById("runSimulationButton");

const resetButton =
    document.getElementById("resetButton");

const currentRoundElement =
    document.getElementById("currentRound");

const aliveNodesElement =
    document.getElementById("aliveNodes");

const deadNodesElement =
    document.getElementById("deadNodes");

const residualEnergyElement =
    document.getElementById("residualEnergy");

const networkVisualization =
    document.getElementById("networkVisualization");

const chHistoryTable =
    document.getElementById("chHistoryTable");


// ============================================================
// 6_05 - NAVIGATION
// ============================================================

const navigationLinks =
    document.querySelectorAll(".nav-item");


navigationLinks.forEach(
    function (link) {

        link.addEventListener(
            "click",
            function () {

                navigationLinks.forEach(
                    function (item) {

                        item.classList.remove(
                            "active"
                        );

                    }
                );


                this.classList.add(
                    "active"
                );

            }
        );

    }
);


// ============================================================
// 6_06 - GET SIMULATION PARAMETERS
// ============================================================

function getSimulationParameters() {

    return {

        numberOfNodes:
            Number(
                nodeCountInput.value
            ),

        initialEnergy:
            Number(
                initialEnergyInput.value
            ),

        chProbability:
            Number(
                chProbabilityInput.value
            ),

        packetSize:
            Number(
                packetSizeInput.value
            ),

        areaX:
            Number(
                areaXInput.value
            ),

        areaY:
            Number(
                areaYInput.value
            ),

        areaZ:
            Number(
                areaZInput.value
            ),

        bsX:
            Number(
                bsXInput.value
            ),

        bsY:
            Number(
                bsYInput.value
            ),

        bsZ:
            Number(
                bsZInput.value
            )

    };

}


// ============================================================
// 6_07 - VALIDATE PARAMETERS
// ============================================================

function validateParameters(
    parameters
) {

    if (
        !Number.isFinite(
            parameters.numberOfNodes
        )
        ||
        parameters.numberOfNodes < 10
    ) {

        alert(
            "Number of nodes must be at least 10."
        );

        return false;

    }


    if (
        !Number.isFinite(
            parameters.initialEnergy
        )
        ||
        parameters.initialEnergy <= 0
    ) {

        alert(
            "Initial energy must be greater than 0."
        );

        return false;

    }


    if (
        !Number.isFinite(
            parameters.chProbability
        )
        ||
        parameters.chProbability <= 0
        ||
        parameters.chProbability > 0.50
    ) {

        alert(
            "CH probability must be between 0.01 and 0.50."
        );

        return false;

    }


    if (
        !Number.isFinite(
            parameters.packetSize
        )
        ||
        parameters.packetSize <= 0
    ) {

        alert(
            "Packet size must be greater than 0."
        );

        return false;

    }


    if (
        parameters.areaX <= 0
        ||
        parameters.areaY <= 0
        ||
        parameters.areaZ <= 0
    ) {

        alert(
            "Network dimensions must be greater than 0."
        );

        return false;

    }


    return true;

}


// ============================================================
// 6_08 - BUTTON RUNNING STATE
// ============================================================

function setSimulationRunningState(
    running
) {

    if (running) {

        runSimulationButton.disabled =
            true;

        runSimulationButton.textContent =
            "Running Simulation...";

    }

    else {

        runSimulationButton.disabled =
            false;

        runSimulationButton.textContent =
            "Run Simulation";

    }

}


// ============================================================
// 6_09 - UPDATE BASIC STATISTICS
// ============================================================

function updateBasicStatistics(
    data
) {

    const metrics =
        data.metrics || [];

    const finalResults =
        data.finalResults || {};


    // --------------------------------------------------------
    // Final results
    // --------------------------------------------------------

    let finalRound =
        finalResults.finalRound ??
        finalResults.round ??
        finalResults.totalRounds;


    let aliveNodes =
        finalResults.aliveNodes ??
        finalResults.alive ??
        finalResults.alive_nodes;


    let deadNodes =
        finalResults.deadNodes ??
        finalResults.dead ??
        finalResults.dead_nodes;


    let residualEnergy =
        finalResults.residualEnergy ??
        finalResults.totalEnergy ??
        finalResults.energy;


    // --------------------------------------------------------
    // Use final metrics row if needed
    // --------------------------------------------------------

    if (
        metrics.length > 0
    ) {

        const lastMetric =
            metrics[
                metrics.length - 1
            ];


        if (
            finalRound === undefined
        ) {

            finalRound =
                lastMetric.Round ??
                lastMetric.round ??
                lastMetric.RoundNumber;

        }


        if (
            aliveNodes === undefined
        ) {

            aliveNodes =
                lastMetric.AliveNodes ??
                lastMetric.aliveNodes ??
                lastMetric.Alive ??
                lastMetric.alive;

        }


        if (
            deadNodes === undefined
        ) {

            deadNodes =
                lastMetric.DeadNodes ??
                lastMetric.deadNodes ??
                lastMetric.Dead ??
                lastMetric.dead;

        }


        if (
            residualEnergy === undefined
        ) {

            residualEnergy =
                lastMetric.TotalEnergy ??
                lastMetric.totalEnergy ??
                lastMetric.ResidualEnergy ??
                lastMetric.residualEnergy ??
                lastMetric.Energy;

        }

    }


    // --------------------------------------------------------
    // Update dashboard
    // --------------------------------------------------------

    if (
        finalRound !== undefined
    ) {

        currentRoundElement.textContent =
            finalRound;

    }


    if (
        aliveNodes !== undefined
    ) {

        aliveNodesElement.textContent =
            aliveNodes;

    }


    if (
        deadNodes !== undefined
    ) {

        deadNodesElement.textContent =
            deadNodes;

    }


    if (
        residualEnergy !== undefined
    ) {

        const energyNumber =
            Number(
                residualEnergy
            );


        if (
            Number.isFinite(
                energyNumber
            )
        ) {

            residualEnergyElement.textContent =
                energyNumber.toFixed(4);

        }

        else {

            residualEnergyElement.textContent =
                residualEnergy;

        }

    }

}


// ============================================================
// 6_10 - DISPLAY NETWORK INFORMATION
// ============================================================

function updateNetworkInformation(
    data
) {

    const nodes =
        data.nodes || [];

    const baseStation =
        data.baseStation || {};


    if (
        !networkVisualization
    ) {

        return;

    }


    networkVisualization.innerHTML =
        "";


    const information =
        document.createElement(
            "div"
        );


    information.style.padding =
        "25px";

    information.style.color =
        "#ffffff";

    information.style.fontSize =
        "15px";


    information.innerHTML = `

        <h3>
            Simulation Completed
        </h3>

        <p>
            Final Nodes:
            <strong>
                ${nodes.length}
            </strong>
        </p>

        <p>
            Base Station:
            <strong>
                (${baseStation.x ?? "-"},
                 ${baseStation.y ?? "-"},
                 ${baseStation.z ?? "-"})
            </strong>
        </p>

        <p>
            CH and Main CH information
            has been received from Python.
        </p>

    `;


    networkVisualization.appendChild(
        information
    );

}


// ============================================================
// 6_11 - DISPLAY CH HISTORY
// ============================================================

function updateCHHistory(
    data
) {

    if (
        !chHistoryTable
    ) {

        return;

    }


    const history =
        data.chHistory || [];


    chHistoryTable.innerHTML =
        "";


    if (
        history.length === 0
    ) {

        const row =
            document.createElement(
                "tr"
            );


        row.innerHTML = `

            <td colspan="5">
                No CH history returned.
            </td>

        `;


        chHistoryTable.appendChild(
            row
        );

        return;

    }


    // --------------------------------------------------------
    // Get column names
    // --------------------------------------------------------

    const firstRow =
        history[0];


    const columns =
        Object.keys(
            firstRow
        );


    // --------------------------------------------------------
    // Header
    // --------------------------------------------------------

    const headerRow =
        document.createElement(
            "tr"
        );


    columns.forEach(
        function (column) {

            const th =
                document.createElement(
                    "th"
                );


            th.textContent =
                column;


            headerRow.appendChild(
                th
            );

        }
    );


    chHistoryTable.appendChild(
        headerRow
    );


    // --------------------------------------------------------
    // Rows
    // --------------------------------------------------------

    history.forEach(
        function (historyRow) {

            const row =
                document.createElement(
                    "tr"
                );


            columns.forEach(
                function (column) {

                    const td =
                        document.createElement(
                            "td"
                        );


                    const value =
                        historyRow[column];


                    if (
                        Array.isArray(
                            value
                        )
                    ) {

                        td.textContent =
                            value.join(
                                ", "
                            );

                    }

                    else if (
                        value === null
                        ||
                        value === undefined
                    ) {

                        td.textContent =
                            "";

                    }

                    else {

                        td.textContent =
                            value;

                    }


                    row.appendChild(
                        td
                    );

                }
            );


            chHistoryTable.appendChild(
                row
            );

        }
    );

}


// ============================================================
// 6_12 - DISPLAY SIMULATION RESULT
// ============================================================

function displaySimulationResult(
    data
) {

    console.log(
        "Full simulation response:",
        data
    );


    updateBasicStatistics(
        data
    );


    updateNetworkInformation(
        data
    );


    updateCHHistory(
        data
    );

}


// ============================================================
// 6_13 - RUN REAL PYTHON SIMULATION
// ============================================================

async function runSimulation() {

    const parameters =
        getSimulationParameters();


    // --------------------------------------------------------
    // Validate parameters
    // --------------------------------------------------------

    if (
        !validateParameters(
            parameters
        )
    ) {

        return;

    }


    // --------------------------------------------------------
    // Change button state
    // --------------------------------------------------------

    setSimulationRunningState(
        true
    );


    try {

        console.log(
            "Sending parameters to Python:"
        );

        console.log(
            parameters
        );


        // ----------------------------------------------------
        // Send request to Flask
        // ----------------------------------------------------

        const response =
            await fetch(
                `${BACKEND_URL}/api/run-simulation`,
                {

                    method:
                        "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(
                            parameters
                        )

                }
            );


        // ----------------------------------------------------
        // Read JSON response
        // ----------------------------------------------------

        const data =
            await response.json();


        console.log(
            "Python response:",
            data
        );


        // ----------------------------------------------------
        // Backend error
        // ----------------------------------------------------

        if (
            !response.ok
            ||
            data.success === false
        ) {

            throw new Error(
                data.error ||
                "Simulation failed."
            );

        }


        // ----------------------------------------------------
        // Display results
        // ----------------------------------------------------

        displaySimulationResult(
            data
        );


        alert(
            "Simulation completed successfully."
        );

    }


    catch (error) {

        console.error(
            "Simulation error:",
            error
        );


        alert(
            "Simulation failed:\n\n"
            +
            error.message
        );

    }


    finally {

        setSimulationRunningState(
            false
        );

    }

}


// ============================================================
// 6_14 - RESET DASHBOARD
// ============================================================

function resetDashboard() {

    currentRoundElement.textContent =
        "0";

    aliveNodesElement.textContent =
        "0";

    deadNodesElement.textContent =
        "0";

    residualEnergyElement.textContent =
        "0 J";


    if (
        networkVisualization
    ) {

        networkVisualization.innerHTML = `

            <div class="empty-state">

                <div class="empty-icon">
                    +
                </div>

                <h3>
                    Network Visualization
                </h3>

                <p>
                    Run the simulation to
                    visualize the network.
                </p>

            </div>

        `;

    }


    if (
        chHistoryTable
    ) {

        chHistoryTable.innerHTML = `

            <tr>

                <td colspan="5">
                    No simulation data
                </td>

            </tr>

        `;

    }

}


// ============================================================
// 6_15 - BUTTON EVENTS
// ============================================================

if (
    runSimulationButton
) {

    runSimulationButton.addEventListener(
        "click",
        runSimulation
    );

}


if (
    resetButton
) {

    resetButton.addEventListener(
        "click",
        resetDashboard
    );

}


// ============================================================
// 6_16 - INITIAL STATE
// ============================================================

resetDashboard();


// ============================================================
// 6_17 - CONSOLE INFORMATION
// ============================================================

console.log(
    "ANN-LEACH website JavaScript loaded."
);

console.log(
    "Backend:",
    BACKEND_URL
);