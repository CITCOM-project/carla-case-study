# Carla Case Study
Code for our investigation into applying Causal Testing to software systems with unobservable and interacting variables. The repo contains test code, DAGs, and data from the ADSs.
If you do not intend to

## Directory Structure
 - carla_garage - Fork of the [carla_garage repo](https://github.com/autonomousvision/carla_garage) with slight modifications to facilitate data collection (e.g. to change the model of the ego-vehicle)
 - TCP - Fork of the [TCP repo](https://github.com/OpenPerceptionX/TCP) with slight modifications to facilitate data collection and more significant modifications to add pedestrians and customise additional environmental parameters
 - case-studies - Contains the causal testing code for each of our three case studies
 - data - contains the CSV data files necessary for causal testing
 - tcp_instrumental_variables.py - compares estimation between instrumental variables and classical adjustment for the TCP data

## Replication
The following steps give instructions on how to reproduce our results. If you would like to re-collect our data, you should follow the steps in order. This will require a PC which meets the [recommended hardware requirements for CARLA](https://github.com/carla-simulator/carla/tree/dev#documentation), and will take a long time (upwards of two weeks) to complete and produce a lot of data.
N.B. Due to the nondeterministic nature of CARLA pedestrian behaviour, the data may not be exactly the same as what we used, but should give similar results and lead to the same conclusions.

We also make our exact data available. To do this, you can simply follow the instructions in `studied-cases/README.md`.

## Setup
1. Install [Anaconda](https://www.anaconda.com/download/) if you do not already have it.
2. Setup CARLA v0.9.10.1:
   ```
   mkdir CARLA-10 &
   cd CARLA-10 &
   wget https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.10.1.tar.gz &
   tar -xf CARLA_0.9.10.1.tar.gz &
   rm CARLA_0.9.10.1.tar.gz
   ```
3. Setup CARLA v0.9.11:
   ```
   mkdir CARLA-11 &
   cd CARLA-11 &
   wget https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.11.tar.gz &
   tar -xf CARLA_0.9.11.tar.gz &
   rm CARLA_0.9.11.tar.gz
   ```
4. Setup TCP:
   ```
   cd TCP & conda env create -f environment.yml --name TCP
   ```
5. Setup CARLA Garage:
   ```
   cd carla_garage & conda env create -f environment.yml
   ```

## Data Collection
6. Collect data for the TCP trained agent with CARLA 10:

   Terminal 1:
   ```
   cd CARLA-10
   ./CarlaUE4.sh --world-port=2000
   ```
   Terminal 2:
   ```
   cd TCP
   conda activate TCP
   bash leaderboard/scripts/run_routes.sh 10
   ```
7. Collect data for the TCP trained agent with CARLA 11:

   Terminal 1:
   ```
   cd CARLA-11
   ./CarlaUE4.sh --world-port=2000
   ```
   Terminal 2:
   ```
   cd TCP
   conda activate TCP
   bash leaderboard/scripts/run_routes.sh 11
   ```
8. Convert the data into a CSV file for causal testing:
   ```
   conda deactivate
   python combine_results.py
   mv results/data.csv ../studied-cases/data/TCP_trained.csv
   ```
9. Collect data for the TCP privileged agent.
  1. Open `TCP/leaderboard/scripts/data_collection.sh`, comment out lines 59 and 60, and uncomment lines 57 and 58 to obtain the following:
  ```
  export TEAM_AGENT=team_code/roach_ap_agent.py
  export TEAM_CONFIG=roach/config/config_agent.yaml
  # export TEAM_AGENT=team_code/tcp_agent.py
  # export TEAM_CONFIG="TCP-agent/epoch=59-last.ckpt"
  ```
  2. Repeat steps 5 and 6
  3. Convert the data into a CSV file for causal testing:
     ```
     conda deactivate
     python combine_results.py
     mv results/data.csv ../studied-cases/data/TCP_privileged.csv
     ```
10. Collect data for CARLA Garage with CARLA 10:

   Terminal 1:
   ```
   cd CARLA-10
   ./CarlaUE4.sh --world-port=2000
   ```
   Terminal 2:
   ```
   cd TCP
   conda activate TCP
   bash leaderboard/scripts/run_routes_scenarios.sh 10
   ```
11. Collect data for CARLA Garage with CARLA 11:
   Terminal 1:
   ```
   cd CARLA-11
   ./CarlaUE4.sh --world-port=2000
   ```
   Terminal 2:
   ```
   cd TCP
   conda activate TCP
   bash leaderboard/scripts/run_routes_scenarios.sh 11
   ```
12. Convert the data into a CSV file for causal testing:
    ```
    conda deactivate
    python combine_results.py
    mv results/data.csv ../studied-cases/data/garage_trained.csv
    ```
13. Collect data for the TCP privileged agent.
   1. Open `TCP/leaderboard/scripts/data_collection.sh`, comment out lines 59 and 60, and uncomment lines 57 and 58 to obtain the following:
   ```
   export TEAM_AGENT=team_code/roach_ap_agent.py
   export TEAM_CONFIG=roach/config/config_agent.yaml
   # export TEAM_AGENT=team_code/tcp_agent.py
   # export TEAM_CONFIG="TCP-agent/epoch=59-last.ckpt"
   ```
   2. Repeat steps 5 and 6, executing `bash leaderboard/scripts/run_routes_scenarios_privileged.sh` instead of `bash leaderboard/scripts/run_routes_scenarios.sh`.
   3. Convert the data into a CSV file for causal testing:
      ```
      conda deactivate
      python combine_results.py
      mv results/data.csv ../studied-cases/data/garage_privileged.csv
      ```
## Causal Testing
14. Perform causal testing according to `studied-cases/README.md`
