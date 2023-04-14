rm case-study-$1/tests.log
python case-study-$1/run_causal_tests.py \
--data_path ../data/TCP_random_vehicle_infractions.csv \
--dag_path case-study-$1/dag.dot \
--json_path case-study-$1/causal_tests.json \
--log_path case-study-$1/tests.log
