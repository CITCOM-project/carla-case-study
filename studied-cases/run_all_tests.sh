for case in 1 2 3
do
  for ads in TCP garage
  do
    for agent in privileged trained
    do
      driver=${ads}_${agent}
      python run_causal_tests.py --dag_path dag.dot --tests_path case-${case}/causal_tests.json --variables case-${case}/variables.json --data_path data/${driver}_data.csv --output_path case-${case}/results/${driver}_results.json
    done
  done
done
