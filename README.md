# Carla Case Study

Code for our investigation into testing autonomous driving systems (ADSs) in the context of CARLA. The repo contains test code, DAGs, and data from the ADSs. We also have submodules for our forks of the ADSs.

## Directory Structure
 - InterFuser - Fork of the [InterFuser repo](https://github.com/opendilab/InterFuser/) with slight modifications to facilitate data collection
 - TCP - Fork of the [TCP repo](https://github.com/OpenPerceptionX/TCP) with slight modifications to facilitate data collection and more significant modifications to add pedestrians and customise additional environmental parameters
 - case-studies - Contains the causal testing code for each of our three case studies
 - data - contains the CSV data files necessary for causal testing
 - tcp_instrumental_variables.py - compares estimation between instrumental variables and classical adjustment for the TCP data
