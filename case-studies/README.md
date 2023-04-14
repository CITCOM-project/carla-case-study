This directory contains the causal tests for each of our three case studies. Each case study can be run by calling `bash run_case_study.sh $study` from this directory, where `$study` is the number of the case study you wish to run, e.g. `bash run_case_study.sh 1`. The output will then be written to `case-study-$study/tests.log`.

Each case study has its own `run_causal_tests.py` script in the interest of clarity, however these could be combined into a single script by combining the lists of inputs and outputs.
