# Case Studies

This directory contains the causal tests for each of our three case studies. To run the causal tests, please follow the following steps:

1. Install [Anaconda](https://www.anaconda.com/download/) if you do not already have it.
2. From the root directory: `conda env create -f environment.yml --name ADStesting`
3. `conda activate ADStesting`
5. Run the causal tests for each case with `bash run_all_tests.sh`. The results will be output to `case-${case}/results/${driver}_results.json`, where `${case}` is the case number (1, 2, or 3), and `${driver}` is `[TCP|garage]-[privileged|trained].`
