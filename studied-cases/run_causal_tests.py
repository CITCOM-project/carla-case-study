import os
from pathlib import Path
import argparse
import json
import pandas as pd
from causal_testing.specification.scenario import Scenario
from causal_testing.specification.variable import Input, Output
from causal_testing.testing.causal_test_outcome import Positive, Negative, NoEffect, SomeEffect, ExactValue
from causal_testing.testing.estimators import LinearRegressionEstimator, InstrumentalVariableEstimator
from causal_testing.json_front.json_class import JsonUtility
from enum import Enum


class ValidationError(Exception):
    """
    Custom class to capture validation errors in this script
    """

    pass


class Infraction(Enum):
    red_light = "red_light"
    collisions_vehicle = "collisions_vehicle"
    collisions_layout = "collisions_layout"
    collisions_pedestrian = "collisions_pedestrian"
    route_timeout = "route_timeout"
    outside_route_lanes = "outside_route_lanes"
    vehicle_blocked = "vehicle_blocked"
    none = "none"

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented


def get_args(test_args=None) -> argparse.Namespace:
    """
    Function to parse arguments from the user using the CLI
    :param test_args: None
    :returns:
            - argparse.Namespace - A Namsespace consisting of the arguments to this script
    """
    parser = argparse.ArgumentParser(description="A script for running the causal testing famework on DAFNI.")

    parser.add_argument("--data_path", required=True, help="Path to the input runtime data (.csv)", nargs="+")

    parser.add_argument(
        "--tests_path", required=True, help="Path to the input configuration file containing the causal tests (.json)"
    )

    parser.add_argument(
        "--variables_path",
        required=True,
        help="Path to the input configuration file containing the predefined variables (.json)",
    )

    parser.add_argument(
        "--dag_path",
        required=True,
        help="Path to the input file containing a valid DAG (.dot). "
        "Note: this must be supplied if the --tests argument isn't provided.",
    )

    parser.add_argument("--output_path", required=False, help="Path to the output directory.")

    parser.add_argument(
        "-f", default=False, help="(Optional) Failure flag to step the framework from running if a test has failed."
    )

    parser.add_argument(
        "-w",
        default=False,
        help="(Optional) Specify to overwrite any existing output files. "
        "This can lead to the loss of existing outputs if not "
        "careful",
    )

    args = parser.parse_args(test_args)

    # Convert these to Path objects for main()

    args.variables_path = Path(args.variables_path)

    args.tests_path = Path(args.tests_path)

    if args.dag_path is not None:
        args.dag_path = Path(args.dag_path)

    if args.output_path is None:
        args.output_path = "./causal_tests_results.json"

        Path(args.output_path).parent.mkdir(exist_ok=True)

    else:
        args.output_path = Path(args.output_path)

        args.output_path.parent.mkdir(exist_ok=True)

    return args


def read_variables(variables_path: Path) -> dict:
    """
    Function to read the variables.json file specified by the user
    :param variables_path: A Path object of the user-specified file path
    :returns:
            - dict - A valid dictionary consisting of the causal tests
    """
    if not variables_path.exists() or variables_path.is_dir():
        raise FileNotFoundError

        print(f"JSON file not found at the specified location: {variables_path}")

    else:
        with variables_path.open("r") as file:
            inputs = json.load(file)

        return inputs


def validate_variables(data_dict: dict) -> tuple:
    """
    Function to validate the variables defined in the causal tests
    :param data_dict: A dictionary consisting of the pre-defined variables for the causal tests
    :returns:
            - tuple - Tuple consisting of the inputs, outputs and constraints to pass into the modelling scenario
    """
    if data_dict["variables"]:
        variables = data_dict["variables"]

        inputs = [
            Input(variable["name"], eval(variable["datatype"]))
            for variable in variables
            if variable["typestring"] == "Input"
        ]

        outputs = [
            Output(
                variable["name"],
                eval(variable["datatype"]),
                hidden=variable["hidden"] if "hidden" in variable else False,
            )
            for variable in variables
            if variable["typestring"] == "Output"
        ]

        constraints = set()

        for variable, _inputs in zip(variables, inputs):
            if "constraint" in variable:
                constraints.add(_inputs.z3 == variable["constraint"])

    else:
        raise ValidationError("Cannot find the variables defined by the causal tests.")

    return inputs, outputs, constraints


def iv_estimator(**kwargs):
    return InstrumentalVariableEstimator(**kwargs, instrument="route_length")


def main():
    """
    Main entrypoint of the script:
    """
    args = get_args()

    try:
        # Step 0: Read in the runtime dataset(s)

        data_frame = pd.concat([pd.read_csv(d) for d in args.data_path])

        # Step 1: Read in the JSON input/output variables and parse io arguments

        variables_dict = read_variables(args.variables_path)

        inputs, outputs, constraints = validate_variables(variables_dict)

        # Step 2: Set up the modeling scenario and estimator

        modelling_scenario = Scenario(variables=inputs + outputs, constraints=constraints)

        modelling_scenario.setup_treatment_variables()

        estimators = {
            "LinearRegressionEstimator": LinearRegressionEstimator,
            "InstrumentalVariableEstimator": iv_estimator,
        }

        # Step 3: Define the expected variables

        expected_outcome_effects = {
            "Positive": Positive(),
            "Negative": Negative(),
            "NoEffect": NoEffect(),
            "SomeEffect": SomeEffect(),
            "1.0": ExactValue(1.0),
            "0.8": ExactValue(0.8),
            "0.7": ExactValue(0.7),
            "0.65": ExactValue(0.65),
            "0.6": ExactValue(0.6),
            "0.5": ExactValue(0.5),
            "-0.01": ExactValue(-0.01, atol=0.1),
            "-0.007": ExactValue(-0.007, atol=0.1),
            "-0.0065": ExactValue(-0.0065, atol=0.1),
            "-0.006": ExactValue(-0.006, atol=0.1),
            "-0.005": ExactValue(-0.005, atol=0.1),
        }

        # Step 4: Call the JSONUtility class to perform the causal tests

        json_utility = JsonUtility(args.output_path, output_overwrite=True)

        # Step 5: Set the path to the data.csv, dag.dot and causal_tests.json file
        json_utility.set_paths(args.tests_path, args.dag_path, args.data_path)

        # Step 6: Sets up all the necessary parts of the json_class needed to execute tests
        json_utility.setup(scenario=modelling_scenario, data=data_frame)

        # Step 7: Run the causal tests
        test_outcomes = json_utility.run_json_tests(
            effects=expected_outcome_effects, mutates={}, estimators=estimators, f_flag=args.f
        )

        # Step 8: Update, print and save the final outputs

        for test in test_outcomes:
            test.pop("estimator")

            if "result" in test:
                test["estimator"] = test["result"].estimator.__class__.__name__

                test["result"] = test["result"].to_dict(json=True)

                test["result"].pop("treatment_value")

                test["result"].pop("control_value")

        with open(args.output_path, "w") as f:
            print(json.dumps(test_outcomes, indent=2), file=f)

        print(json.dumps(test_outcomes, indent=2))

        df = json_utility.data_collector.data
        for infraction in set(df.infraction_name):
            print(infraction, len(df.query(f"infraction_name == '{infraction}'")))

    except ValidationError as ve:
        print(f"Cannot validate the specified input configurations: {ve}")

    else:
        print(f"Execution successful. Output file saved at {Path(args.output_path).parent.resolve()}")


if __name__ == "__main__":
    main()
