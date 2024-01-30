# Case Study 1
In this case, we validate that TCP and CARLA Garage can drive another ego vehicle other than the Lincoln MKZ2017.

# Execution
To run this case study for TCP:
```
python run_causal_tests.py --dag_path dag.dot --tests_path case-2/causal_tests.json --variables case-2/variables.json --data_path data/TCP_data.csv --output_path case-2/TCP_results.json
```

To run this case study for CARLA Garage:
```
python run_causal_tests.py --dag_path dag.dot --tests_path case-2/causal_tests.json --variables case-2/variables.json --data_path data/garage_data.csv --output_path case-2/garage_results.json
```

# Interpretation
Here, we see that the causal tests fail for both ADSs, meaning that the model of the ego vehicle in fact _does_ affect the infraction penalty we can expect to achieve.
