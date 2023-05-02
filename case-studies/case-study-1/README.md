# Case Study 1
In this case study, we validate that TCP and InterFuser are penalising infractions correctly.

To run this case study for TCP:
```
rm TCP-tests.log # if it exists
python run_causal_tests.py \
--data_path ../../data/TCP.csv \
--dag_path dag.dot \
--json_path causal_tests_TCP.json \
--log_path TCP-tests.log
```

To run this case study for InterFuser:
```
rm InterFuser-tests.log # if it exists
python run_causal_tests.py \
--data_path ../../data/InterFuser.csv \
--dag_path dag.dot \
--json_path causal_tests_InterFuser.json \
--log_path InterFuser-tests.log
```

The two JSON test files are the same except in `causal-tests_InterFuser.json`, the test involving pedestrian collisions is skipped due to InterFuser not having the capability to run with pedestrians. Hence, no pedestrian collisions could have taken place.
