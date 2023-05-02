# Case Studies

This directory contains the causal tests for each of our three case studies. To run the causal tests, please follow the following steps:

1. Install [Anaconda](https://www.anaconda.com/download/) if you do not already have it.
2. `conda create -n carlastudy python=3.9`
3. `conda activate carlastudy`
4. `pip install -r requirements.txt`
5. Each case study can be run by executing the python script in each directory according to the instructions in its README.md.

Each case study has its own `run_causal_tests.py` script in the interest of clarity, however these could be combined into a single script by combining the lists of inputs and outputs, thus enabling all three causal test suites to be run with a single python script.
