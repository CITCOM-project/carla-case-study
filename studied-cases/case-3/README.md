# Case Study 1
In this case, we validate that changing the version of CARLA does not significantly affect the simulation time.

# Execution
To run this case study for TCP:
```
python run_causal_tests.py --dag_path dag.dot --tests_path case-3/causal_tests.json --variables case-3/variables.json --data_path data/TCP_data.csv --output_path case-3/TCP_results.json
```

To run this case study for CARLA Garage:
```
python run_causal_tests.py --dag_path dag.dot --tests_path case-3/causal_tests.json --variables case-3/variables.json --data_path data/garage_data.csv --output_path case-3/garage_results.json
```

# Interpretation
From the causal test results, we can see tat the effect estimates of simulation time on system time are almost the same between CARLA 10 and CARLA 11. Thus, we can conclude that changing the CARLA version does not significantly affect performance.
