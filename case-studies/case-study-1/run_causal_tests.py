import numpy as np
import pandas as pd
import scipy
from enum import Enum
from typing import Any
from z3 import And
import statsmodels.api as sm

from causal_testing.specification.variable import Variable
from causal_testing.testing.estimators import (
    LinearRegressionEstimator,
    LogisticRegressionEstimator,
    InstrumentalVariableEstimator,
)
from causal_testing.testing.causal_test_outcome import (
    SomeEffect,
    NoEffect,
    Negative,
    ExactValue,
    Positive,
)
from causal_testing.json_front.json_class import JsonUtility
from causal_testing.testing.estimators import Estimator
from causal_testing.specification.scenario import Scenario
from causal_testing.specification.variable import Input, Output

class Infraction(Enum):
    red_light = "red_light"
    collisions_vehicle = "collisions_vehicle"
    collisions_layout = "collisions_layout"
    collisions_pedestrian = "collisions_pedestrian"
    route_timeout = "route_timeout"
    outside_route_lanes = "outside_route_lanes"
    vehicle_blocked = "vehicle_blocked"
    false = "False"

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

effects = {
    "1.0": ExactValue(1),
    "0.8": ExactValue(0.8),
    "0.7": ExactValue(0.7),
    "0.65": ExactValue(0.65),
    "0.6": ExactValue(0.6),
    "0.5": ExactValue(0.5),
}

outputs = [
{"name": "score_route", "datatype": float},
{"name": "score_composed", "datatype": float},
{"name": "infraction", "datatype": Infraction}
]

# Create input structure required to create a modelling scenario
variables = [Output(i["name"], i["datatype"]) for i in outputs]

vnames = {v.name: v for v in variables}

# Create modelling scenario to access z3 variable mirrors
modelling_scenario = Scenario(variables, constraints = [])
modelling_scenario.setup_treatment_variables()


estimators = {
    "LinearRegressionEstimator": LinearRegressionEstimator,
}

if __name__ == "__main__":
    args = JsonUtility.get_args()
    json_utility = JsonUtility(
        args.log_path
    )  # Create an instance of the extended JsonUtility class
    json_utility.set_paths(
        args.json_path, args.dag_path, args.data_path
    )  # Set the path to the data.csv, dag.dot and causal_tests.json file

    # Load the Causal Variables into the JsonUtility class ready to be used in the tests
    json_utility.setup(scenario=modelling_scenario)  # Sets up all the necessary parts of the json_class needed to execute tests

    json_utility.run_json_tests(effects, mutates={}, estimators=estimators, f_flag=args.f)
