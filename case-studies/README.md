# Case Studies

This directory contains the causal tests for each of our three case studies. To run the causal tests, please follow the following steps:

1. Install [Anaconda](https://www.anaconda.com/download/) if you do not already have it.
2. `conda create -n carlastudy python=3.9`
3. `conda activate carlastudy`
4. `pip install -r requirements.txt`
5. Each case study can be run by calling `bash run-case-study.sh $study` from the `case-studies` directory, where `$study` is the case study you wish to run, e.g. `bash run-case-study.sh 1`. Two log files will then be created in within the `case-study-$study` directory, one for each ADS.<br/>
Alternatively, you can simply call the test runner script directly, e.g. `python case-study-1/run_causal_tests.py --data_path ../data/TCP.csv --dag_path case-study-1/dag.dot --json_path case-study-1/causal_tests.json --log_path case-study-1/tests.log`, which will run the first case study with the TCP data. For the other case studies, simply replace `case-study-1` with `case-study-2` or `case-study-3`, or replace `TCP` with `InterFuser`.

Each case study has its own `run_causal_tests.py` script in the interest of clarity, however these could be combined into a single script by combining the lists of inputs and outputs, thus enabling all three causal test suites to be run with a single python script.
