# Case Study 1
In this case study, we use instrumental variables to investigate runtime.

To run this case study for TCP:
```
rm TCP-tests.log # if it exists
python run_causal_tests.py \
--data_path ../../data/TCP.csv \
--dag_path dag.dot \
--json_path causal_tests.json \
--log_path TCP-tests.log
```

To run this case study for TCP (original data):
```
rm TCP_original-tests.log # if it exists
python run_causal_tests.py \
--data_path ../../data/TCP_original.csv \
--dag_path dag.dot \
--json_path causal_tests.json \
--log_path TCP_original-tests.log
```

To run this case study for InterFuser:
```
rm InterFuser-tests.log # if it exists
python run_causal_tests.py \
--data_path ../../data/InterFuser.csv \
--dag_path dag.dot \
--json_path causal_tests.json \
--log_path InterFuser-tests.log
```
