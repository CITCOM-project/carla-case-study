# Case Study 1
In this case study, we validate that TCP and CARLA Garage can drive another ego vehicle other than the Lincoln MKZ2017.

To run this case study for TCP:
```
python run_causal_tests.py --dag_path dag.dot --tests_path case-2/causal_tests.json --variables case-2/variables.json --data_path data/TCP_data.csv --output_path case-2/TCP_results.json
```

To run this case study for CARLA Garage:
```
python run_causal_tests.py --dag_path dag.dot --tests_path case-2/causal_tests.json --variables case-2/variables.json --data_path data/garage_data.csv --output_path case-2/garage_results.json
```
