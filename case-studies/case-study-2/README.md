# Case Study 1
In this case study, we use exploratory testing to discover the route cause of missing data values.

We only encountered missing data values for TCP, so it only applies to TCP:
```
rm TCP-tests.log # if it exists
python run_causal_tests.py \
--data_path ../../data/TCP.csv \
--dag_path dag.dot \
--json_path causal_tests_TCP.json \
--log_path TCP-tests.log
```

N.B. Tests will fail if applied to the InterFuser data as it does not record the numbers of pedestrians and NPC drivers.
