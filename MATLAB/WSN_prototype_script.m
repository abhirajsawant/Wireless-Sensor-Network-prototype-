%% STEP 1 - 3D WSN SETUP AND NODE DEPLOYMENT
% WSN  = Wireless Sensor Network
% BS   = Base Station
% SN   = Sensor Nodes
% Eo   = Initial Energy
% Job  : Create the 3D network, deploy nodes, calculate BS distance,
%        and display the initial network.

clear;
clc;
close all;

%% 1. NETWORK PARAMETERS
% Working: Define the number of nodes, network dimensions,
%          initial node energy, and Base Station position.

SN = 100;

area_x = 100;
area_y = 100;
area_z = 100;

Eo = 0.5;

BS.x = 50;
BS.y = 50;
BS.z = 0;

%% 2. NODE STRUCTURE
% Working: Store position, energy, CH information,
%          and Main CH information for every sensor node.

node = struct( ...
    'x',0,'y',0,'z',0, ...
    'energy',0, ...
    'distanceBS',0, ...
    'avgClusterEnergy',0, ...
    'CH_x',0,'CH_y',0,'CH_z',0, ...
    'isCH',false, ...
    'isMainCH',false);

%% 3. 3D NODE DEPLOYMENT
% Working: Randomly deploy every sensor node inside
%          the 100 x 100 x 100 m network area.

for i = 1:SN

    node(i).x = rand * area_x;
    node(i).y = rand * area_y;
    node(i).z = rand * area_z;

    node(i).energy = Eo;

    %% Distance from node to BS
    % Working: Calculate 3D Euclidean distance between
    %          each sensor node and the Base Station.

    node(i).distanceBS = sqrt( ...
        (node(i).x - BS.x)^2 + ...
        (node(i).y - BS.y)^2 + ...
        (node(i).z - BS.z)^2);

end

%% 4. INITIAL NETWORK ENERGY
% Working: Calculate the average initial energy of all nodes.

initialAvgEnergy = mean([node.energy]);

for i = 1:SN
    node(i).avgClusterEnergy = initialAvgEnergy;
end

%% 5. NODE INFORMATION PACKET
% Packet = Information carried/used for node processing.
% Columns:
% 1 = X position
% 2 = Y position
% 3 = Z position
% 4 = Residual energy
% 5 = Distance to BS
% 6 = Average cluster energy
% 7 = CH X position
% 8 = CH Y position
% 9 = CH Z position

NodeInfo_Packet = zeros(SN,9);

for i = 1:SN

    NodeInfo_Packet(i,:) = [ ...
        node(i).x, ...
        node(i).y, ...
        node(i).z, ...
        node(i).energy, ...
        node(i).distanceBS, ...
        node(i).avgClusterEnergy, ...
        node(i).CH_x, ...
        node(i).CH_y, ...
        node(i).CH_z];

end

X = NodeInfo_Packet;

%% 6. INITIAL 3D NETWORK VISUALIZATION
% Working: Display sensor nodes and the Base Station
%          in the 3D simulation environment.

figure;

scatter3( ...
    [node.x], ...
    [node.y], ...
    [node.z], ...
    45, ...
    'b', ...
    'filled');

hold on;

% Display Base Station
scatter3( ...
    BS.x, ...
    BS.y, ...
    BS.z, ...
    100, ...
    'r', ...
    'filled');

xlabel('X (m)');
ylabel('Y (m)');
zlabel('Z (m)');

title('3D Wireless Sensor Network Deployment');

grid on;

axis([ ...
    0 area_x ...
    0 area_y ...
    0 area_z]);

view(3);

hold off;

%% STEP 2 - ANN1 INPUT PREPARATION AND CH SELECTION
% ANN  = Artificial Neural Network
% ANN1 = First Artificial Neural Network
% CH   = Cluster Head
% Job  : Prepare the first ANN inputs, normalize the data,
%        generate the reference suitability target, train ANN1,
%        calculate ANN scores, and select Cluster Heads.

%% 1. ANN1 INPUTS
% Working: Use the first 6 features from the Node Information Packet.
% Features:
% X, Y, Z, Energy, Distance to BS, Average Cluster Energy

ANN1_Input = X(:,1:6);

%% 2. MIN-MAX NORMALIZATION
% Working: Convert every input feature into the range [0,1].

inputMin = min(ANN1_Input);
inputMax = max(ANN1_Input);

inputRange = inputMax - inputMin;

ANN1_Input_Norm = zeros(size(ANN1_Input));

for j = 1:6

    if inputRange(j) == 0
        ANN1_Input_Norm(:,j) = 0.5;
    else
        ANN1_Input_Norm(:,j) = ...
            (ANN1_Input(:,j) - inputMin(j)) / inputRange(j);
    end

end

%% 3. ANN1 REFERENCE SUITABILITY TARGET
% Working: Create the prototype target used to train ANN1.
% Energy              = 40%
% Distance to BS      = 30%
% Average Cluster Energy = 30%

energyScore = ANN1_Input_Norm(:,4);

distanceScore = 1 - ANN1_Input_Norm(:,5);

clusterEnergyScore = ANN1_Input_Norm(:,6);

ANN1_Target = ...
    0.4 * energyScore + ...
    0.3 * distanceScore + ...
    0.3 * clusterEnergyScore;

%% 4. ANN1 TRAINING DATA
% Working: Transpose the data into the format required by feedforwardnet.

ANN1_Input_Train = ANN1_Input_Norm';
ANN1_Target_Train = ANN1_Target';

%% 5. CREATE AND TRAIN ANN1
% feedforwardnet = Feed-Forward Neural Network
% Working: Create ANN1 with 10 hidden neurons and train it
%          using the reference suitability target.

hiddenNeurons = 10;

net1 = feedforwardnet(hiddenNeurons);

net1 = train( ...
    net1, ...
    ANN1_Input_Train, ...
    ANN1_Target_Train);

%% 6. GENERATE ANN1 SUITABILITY SCORE
% Working: Calculate the suitability score of every sensor node.

ANN1_Output = net1(ANN1_Input_Train)';

%% 7. CLUSTER HEAD SELECTION
% p = Desired percentage of Cluster Heads.
% Working: Select the highest-scoring nodes as CHs.

p = 0.1;

numberOfCH = floor(p * SN);

[sortedScores, sortedIndex] = ...
    sort(ANN1_Output, 'descend');

CH_Index = sortedIndex(1:numberOfCH);

%% 8. STORE CH STATUS
% Working: Mark selected nodes as Cluster Heads.

isCH = false(SN,1);

isCH(CH_Index) = true;

for i = 1:SN
    node(i).isCH = isCH(i);
end

%% STEP 3 - 3D CLUSTER FORMATION
% Cluster = Group of sensor nodes served by one CH
% Job    : Assign every non-CH node to its nearest CH
%          using 3D Euclidean distance.

%% 1. INITIALIZE CLUSTERS

Clusters = cell(numberOfCH,1);

for k = 1:numberOfCH
    Clusters{k} = CH_Index(k);
end

%% 2. ASSIGN NON-CH NODES TO NEAREST CH

for i = 1:SN

    if ~isCH(i)

        minDistance = inf;
        nearestCH = 0;

        for k = 1:numberOfCH

            ch = CH_Index(k);

            distance3D = sqrt( ...
                (node(i).x - node(ch).x)^2 + ...
                (node(i).y - node(ch).y)^2 + ...
                (node(i).z - node(ch).z)^2);

            if distance3D < minDistance

                minDistance = distance3D;
                nearestCH = ch;

            end

        end

        Clusters{find(CH_Index == nearestCH)}(end+1) = i;

        node(i).CH_x = node(nearestCH).x;
        node(i).CH_y = node(nearestCH).y;
        node(i).CH_z = node(nearestCH).z;

    else

        node(i).CH_x = node(i).x;
        node(i).CH_y = node(i).y;
        node(i).CH_z = node(i).z;

    end

end

%% 3. CLUSTER INFORMATION

clusterSize = zeros(numberOfCH,1);
clusterEnergy = zeros(numberOfCH,1);

for k = 1:numberOfCH

    members = Clusters{k};

    clusterSize(k) = length(members);

    clusterEnergy(k) = sum([node(members).energy]);

end

%% 4. UPDATE AVERAGE CLUSTER ENERGY

for k = 1:numberOfCH

    members = Clusters{k};

    avgEnergy = mean([node(members).energy]);

    for j = 1:length(members)

        node(members(j)).avgClusterEnergy = avgEnergy;

    end

end

%% 5. CLUSTER VISUALIZATION

figure;

hold on;

scatter3( ...
    [node(~isCH).x], ...
    [node(~isCH).y], ...
    [node(~isCH).z], ...
    35, ...
    'b', ...
    'filled');

scatter3( ...
    [node(isCH).x], ...
    [node(isCH).y], ...
    [node(isCH).z], ...
    90, ...
    'r', ...
    'filled');

scatter3( ...
    BS.x, ...
    BS.y, ...
    BS.z, ...
    120, ...
    'k', ...
    'filled');

for k = 1:numberOfCH

    ch = CH_Index(k);
    members = Clusters{k};

    for j = 1:length(members)

        n = members(j);

        if n ~= ch

            plot3( ...
                [node(n).x node(ch).x], ...
                [node(n).y node(ch).y], ...
                [node(n).z node(ch).z], ...
                'k-');

        end

    end

end

xlabel('X (m)');
ylabel('Y (m)');
zlabel('Z (m)');

title('3D Cluster Formation');

grid on;
axis([0 area_x 0 area_y 0 area_z]);
view(3);

hold off;

%% STEP 4 - ANN2 AND MAIN CH SELECTION
% ANN2 = Second Artificial Neural Network
% MCH  = Main Cluster Head
% Job  : Evaluate Cluster Heads using residual energy,
%        distance to BS, and cluster size, then select MCHs.

%% 1. ANN2 INPUT PREPARATION

ANN2_Input = zeros(numberOfCH,6);

for k = 1:numberOfCH

    ch = CH_Index(k);

    ANN2_Input(k,1) = node(ch).x;
    ANN2_Input(k,2) = node(ch).y;
    ANN2_Input(k,3) = node(ch).z;
    ANN2_Input(k,4) = node(ch).energy;
    ANN2_Input(k,5) = node(ch).distanceBS;
    ANN2_Input(k,6) = clusterSize(k);

end

%% 2. ANN2 NORMALIZATION

inputMin2 = min(ANN2_Input);
inputMax2 = max(ANN2_Input);

inputRange2 = inputMax2 - inputMin2;

ANN2_Input_Norm = zeros(size(ANN2_Input));

for j = 1:6

    if inputRange2(j) == 0
        ANN2_Input_Norm(:,j) = 0.5;
    else
        ANN2_Input_Norm(:,j) = ...
            (ANN2_Input(:,j) - inputMin2(j)) / inputRange2(j);
    end

end

%% 3. ANN2 REFERENCE TARGET
% Energy              = 40%
% Distance suitability = 30%
% Cluster size         = 30%

energyScore2 = ANN2_Input_Norm(:,4);

distanceScore2 = 1 - ANN2_Input_Norm(:,5);

clusterSizeScore2 = ANN2_Input_Norm(:,6);

ANN2_Target = ...
    0.4 * energyScore2 + ...
    0.3 * distanceScore2 + ...
    0.3 * clusterSizeScore2;

%% 4. TRAIN ANN2

ANN2_Input_Train = ANN2_Input_Norm';
ANN2_Target_Train = ANN2_Target';

net2 = feedforwardnet(10);

net2 = train( ...
    net2, ...
    ANN2_Input_Train, ...
    ANN2_Target_Train);

%% 5. CALCULATE ANN2 SCORES

ANN2_Output = net2(ANN2_Input_Train)';

%% 6. MAIN CH SELECTION
% q = Percentage of selected Main Cluster Heads.

q = 0.1;

numberOfMCH = max(1,floor(q * numberOfCH));

[~,MCH_Sorted_Index] = ...
    sort(ANN2_Output,'descend');

MCH_Position = MCH_Sorted_Index(1:numberOfMCH);

MCH_Index = CH_Index(MCH_Position);

%% 7. STORE MAIN CH STATUS

isMainCH = false(SN,1);

isMainCH(MCH_Index) = true;

for i = 1:SN

    node(i).isMainCH = isMainCH(i);

end

%% 8. DISPLAY ANN SELECTION RESULTS

fprintf('\n============================================\n');
fprintf('ANN1 CLUSTER HEAD SELECTION\n');
fprintf('============================================\n');

fprintf('Total Sensor Nodes : %d\n',SN);
fprintf('Selected CHs       : %d\n',numberOfCH);

fprintf('\nCluster Head IDs:\n');
disp(CH_Index');

fprintf('\n============================================\n');
fprintf('ANN2 MAIN CH SELECTION\n');
fprintf('============================================\n');

fprintf('Total CHs           : %d\n',numberOfCH);
fprintf('Selected Main CHs   : %d\n',numberOfMCH);

fprintf('\nMain Cluster Head IDs:\n');
disp(MCH_Index');

%% 9. 3D CH AND MAIN CH VISUALIZATION

figure;

hold on;

nonCH = ~isCH;

scatter3( ...
    [node(nonCH).x], ...
    [node(nonCH).y], ...
    [node(nonCH).z], ...
    30,'b','filled');

scatter3( ...
    [node(isCH).x], ...
    [node(isCH).y], ...
    [node(isCH).z], ...
    80,'r','filled');

scatter3( ...
    [node(isMainCH).x], ...
    [node(isMainCH).y], ...
    [node(isMainCH).z], ...
    130,'m','filled');

scatter3( ...
    BS.x, ...
    BS.y, ...
    BS.z, ...
    120,'k','filled');

xlabel('X (m)');
ylabel('Y (m)');
zlabel('Z (m)');

title('ANN1 CH and ANN2 Main CH Selection');

legend( ...
    'Sensor Nodes', ...
    'Cluster Heads', ...
    'Main Cluster Heads', ...
    'Base Station');

grid on;

axis([0 area_x 0 area_y 0 area_z]);

view(3);

hold off;

%% STEP 5 - TDMA AND ENERGY MODEL
% TDMA = Time Division Multiple Access
% ETX  = Energy consumed during transmission
% ERX  = Energy consumed during reception
% Efs  = Free-space amplifier energy
% EDA  = Data aggregation energy
% Job  : Define the radio-energy model and prepare
%        communication energy calculations.

%% 1. RADIO PARAMETERS

packetLength = 4000;

ETX = 50e-9;
ERX = 50e-9;
Efs = 10e-12;
EDA = 5e-9;

%% 2. TDMA SCHEDULE
% Working: Each cluster member gets one transmission slot.
%          CHs receive data from their cluster members.

TDMA_Schedule = cell(numberOfCH,1);

for k = 1:numberOfCH

    members = Clusters{k};

    members = members(members ~= CH_Index(k));

    TDMA_Schedule{k} = members;

end

%% 3. NODE TO CH ENERGY CALCULATION

Energy_Node_to_CH = zeros(SN,1);

for k = 1:numberOfCH

    ch = CH_Index(k);

    members = TDMA_Schedule{k};

    for j = 1:length(members)

        n = members(j);

        d = sqrt( ...
            (node(n).x - node(ch).x)^2 + ...
            (node(n).y - node(ch).y)^2 + ...
            (node(n).z - node(ch).z)^2);

        E_TX = ...
            packetLength * ETX + ...
            packetLength * Efs * d^2;

        Energy_Node_to_CH(n) = E_TX;

    end

end

%% 4. CH RECEIVING ENERGY

Energy_CH_RX = zeros(SN,1);

for k = 1:numberOfCH

    ch = CH_Index(k);

    members = TDMA_Schedule{k};

    Energy_CH_RX(ch) = ...
        length(members) * packetLength * ERX;

end

%% 5. CH TO MAIN CH ENERGY

Energy_CH_to_MCH = zeros(SN,1);

for k = 1:numberOfCH

    ch = CH_Index(k);

    if ~isMainCH(ch)

        distances = zeros(numberOfMCH,1);

        for m = 1:numberOfMCH

            mch = MCH_Index(m);

            distances(m) = sqrt( ...
                (node(ch).x - node(mch).x)^2 + ...
                (node(ch).y - node(mch).y)^2 + ...
                (node(ch).z - node(mch).z)^2);

        end

        [d,minIndex] = min(distances);

        targetMCH = MCH_Index(minIndex);

        E_TX_MCH = ...
            packetLength * ETX + ...
            packetLength * Efs * d^2;

        Energy_CH_to_MCH(ch) = E_TX_MCH;

    end

end

%% 6. MAIN CH TO BS ENERGY

Energy_MCH_to_BS = zeros(SN,1);

for m = 1:numberOfMCH

    mch = MCH_Index(m);

    dBS = sqrt( ...
        (node(mch).x - BS.x)^2 + ...
        (node(mch).y - BS.y)^2 + ...
        (node(mch).z - BS.z)^2);

    E_TX_BS = ...
        packetLength * ETX + ...
        packetLength * Efs * dBS^2;

    Energy_MCH_to_BS(mch) = E_TX_BS;

end

%% 7. DATA AGGREGATION ENERGY

Energy_Data_Aggregation = zeros(SN,1);

for k = 1:numberOfCH

    ch = CH_Index(k);

    members = TDMA_Schedule{k};

    Energy_Data_Aggregation(ch) = ...
        length(members) * packetLength * EDA;

end

%% 8. TOTAL ENERGY REQUIRED IN CURRENT ROUND

Energy_Total = ...
    Energy_Node_to_CH + ...
    Energy_CH_RX + ...
    Energy_CH_to_MCH + ...
    Energy_MCH_to_BS + ...
    Energy_Data_Aggregation;

%% STEP 6 - ENERGY UPDATE AND NODE DEATH
% FND = First Node Death
% HND = Half Node Death
% LND = Last Node Death
% Job : Apply communication energy consumption and determine
%       which nodes are alive or dead.

for i = 1:SN

    node(i).energy = node(i).energy - Energy_Total(i);

    if node(i).energy < 0
        node(i).energy = 0;
    end

end

alive = find([node.energy] > 0);
dead  = find([node.energy] <= 0);

aliveCount = length(alive);
deadCount  = length(dead);

%% STEP 7 - PERFORMANCE STORAGE
% Job : Store node lifetime, energy, CH and Main CH information.

round = 1;

aliveNodes = zeros(1,1);
deadNodes = zeros(1,1);
totalEnergy = zeros(1,1);
CH_History = cell(1,1);
MCH_History = cell(1,1);

aliveNodes(round) = aliveCount;
deadNodes(round) = deadCount;
totalEnergy(round) = sum([node.energy]);

CH_History{round} = CH_Index;
MCH_History{round} = MCH_Index;

FND = 0;
HND = 0;
LND = 0;

if aliveCount < SN && FND == 0
    FND = round;
end

if aliveCount <= floor(SN/2) && HND == 0
    HND = round;
end

if aliveCount == 0 && LND == 0
    LND = round;
end

%% STEP 8 - FINAL NETWORK STATUS
% Job : Display the results of the completed simulation round.

fprintf('\n============================================\n');
fprintf('NETWORK PERFORMANCE\n');
fprintf('============================================\n');

fprintf('Simulation Round       : %d\n',round);
fprintf('Alive Nodes             : %d\n',aliveCount);
fprintf('Dead Nodes              : %d\n',deadCount);
fprintf('Total Residual Energy   : %.6f J\n', ...
    totalEnergy(round));

fprintf('\nCH IDs:\n');
disp(CH_Index');

fprintf('Main CH IDs:\n');
disp(MCH_Index');

%% STEP 9 - ENERGY AND NODE STATUS FIGURES
% Job : Display residual energy and alive/dead nodes.

figure;

plot( ...
    1:round, ...
    totalEnergy(1:round), ...
    'LineWidth',2);

xlabel('Round');
ylabel('Residual Energy (J)');
title('Network Residual Energy');

grid on;

figure;

plot( ...
    1:round, ...
    aliveNodes(1:round), ...
    'LineWidth',2);

hold on;

plot( ...
    1:round, ...
    deadNodes(1:round), ...
    'LineWidth',2);

xlabel('Round');
ylabel('Number of Nodes');

title('Alive and Dead Sensor Nodes');

legend('Alive Nodes','Dead Nodes');

grid on;

hold off;

%% STEP 10 - FINAL 3D NETWORK
% Job : Show the final condition of the sensor network.

figure;

hold on;

if ~isempty(alive)

    scatter3( ...
        [node(alive).x], ...
        [node(alive).y], ...
        [node(alive).z], ...
        45,'b','filled');

end

if ~isempty(dead)

    scatter3( ...
        [node(dead).x], ...
        [node(dead).y], ...
        [node(dead).z], ...
        45,'r','filled');

end

scatter3( ...
    [node(CH_Index).x], ...
    [node(CH_Index).y], ...
    [node(CH_Index).z], ...
    90,'g','filled');

scatter3( ...
    [node(MCH_Index).x], ...
    [node(MCH_Index).y], ...
    [node(MCH_Index).z], ...
    120,'m','filled');

scatter3( ...
    BS.x,BS.y,BS.z, ...
    120,'k','filled');

xlabel('X (m)');
ylabel('Y (m)');
zlabel('Z (m)');

title('Final 3D WSN Status');

legend( ...
    'Alive Nodes', ...
    'Dead Nodes', ...
    'Cluster Heads', ...
    'Main Cluster Heads', ...
    'Base Station');

grid on;

axis([0 area_x 0 area_y 0 area_z]);

view(3);

hold off;

%% STEP 11 - LIFETIME RESULTS
% Job : Display the calculated network lifetime indicators.

fprintf('\n============================================\n');
fprintf('NETWORK LIFETIME RESULTS\n');
fprintf('============================================\n');

if FND > 0
    fprintf('First Node Death      : Round %d\n',FND);
else
    fprintf('First Node Death      : Not reached\n');
end

if HND > 0
    fprintf('Half Node Death       : Round %d\n',HND);
else
    fprintf('Half Node Death       : Not reached\n');
end

if LND > 0
    fprintf('Last Node Death       : Round %d\n',LND);
else
    fprintf('Last Node Death       : Not reached\n');
end

fprintf('============================================\n');