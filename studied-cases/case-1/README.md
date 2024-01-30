# Case Study 1
In this case study, we validate that TCP and CARLA Garage are penalising infractions correctly.

To run this case study for TCP:
```
python run_causal_tests.py --dag_path dag.dot --tests_path case-1/causal_tests_TCP.json --variables case-1/variables.json --data_path data/TCP_data.csv --output_path case-1/TCP_results.json
```

To run this case study for CARLA Garage:
```
python run_causal_tests.py --dag_path dag.dot --tests_path case-1/causal_tests_garage.json --variables case-1/variables.json --data_path data/garage_data.csv --output_path case-1/garage_results.json
```

# FIXME
The two JSON test files are the same except in `causal-tests_InterFuser.json`, the test involving pedestrian collisions is skipped due to InterFuser not having the capability to run with pedestrians. Hence, no pedestrian collisions could have taken place.
