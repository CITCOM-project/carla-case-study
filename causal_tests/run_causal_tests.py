import numpy as np
import pandas as pd
import scipy
from enum import Enum
from typing import Any
from z3 import And
import statsmodels.api as sm

from causal_testing.specification.variable import Variable
from causal_testing.testing.estimators import LinearRegressionEstimator, LogisticRegressionEstimator, InstrumentalVariableEstimator
from causal_testing.testing.causal_test_outcome import SomeEffect, NoEffect, Negative, ExactValue, Positive
from causal_testing.json_front.json_class import JsonUtility
from causal_testing.testing.estimators import Estimator
from causal_testing.specification.scenario import Scenario
from causal_testing.specification.variable import Input, Output

Status = Enum('Status', ['Completed', 'Failed', 'Failed - Agent timed out'])

class InfractionsEstimator(Estimator):
    def add_modelling_assumptions(self):
        self.modelling_assumptions += (
            "The variables in the data must fit a shape which can be expressed as a linear"
            "combination of parameters and functions of variables. Note that these functions"
            "do not need to be linear."
        )

    def estimate_ate(self):
        stratum = self.df.where(self.df['infraction'] == self.effect_modifiers["infraction"]).dropna()
        model = sm.OLS(stratum['score_composed'], stratum[["score_route"]]).fit()
        return model.params['score_route'], sorted(model.conf_int(alpha=0.05, cols=None).loc['score_route'])

class Car(Enum):
    isetta = 'vehicle.bmw.isetta'
    mkz2017 = 'vehicle.lincoln.mkz2017'

    def __gt__(self, other):
         if self.__class__ is other.__class__:
           return self.value > other.value
         return NotImplemented


class EnumGen(scipy.stats.rv_discrete):
    def __init__(self, dt: Enum):
        self.dt = dict(enumerate(dt, 1))
        self.inverse_dt = {v:k for k, v in self.dt.items()}

    def ppf(self, q, *args, **kwds):
        return np.vectorize(self.dt.get)(
            np.ceil(len(self.dt) * q)
        )

    def cdf(self, q, *args, **kwds):
        return np.vectorize(self.inverse_dt.get)(q)/len(Car)


class Infraction(Enum):
    red_light = 'red_light'
    # collisions_pedestrian = 'collisions_pedestrian'
    collisions_vehicle = 'collisions_vehicle'
    collisions_layout = 'collisions_layout'
    false = 'False'

    def __gt__(self, other):
         if self.__class__ is other.__class__:
           return self.value > other.value
         return NotImplemented

inputs = [
    {"hidden": True, "name": "percentage_speed_limit", "datatype": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "cloudiness", "datatype": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "fog_density", "datatype": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "fog_distance", "datatype": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "fog_falloff", "datatype": float, "distribution": scipy.stats.uniform(0, 100)},
    {"hidden": True, "name": "number_of_drivers", "datatype": int, "distribution": scipy.stats.rv_discrete(name="drivers", values=(range(0, 200), [1/200]*200))},
    {"hidden": True, "name": "number_of_walkers", "datatype": int, "distribution": scipy.stats.rv_discrete(name="drivers", values=(range(0, 200), [1/200]*200))},
    {"name": "precipitation", "datatype": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "precipitation_deposits", "datatype": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "sun_altitude_angle", "datatype": float, "distribution": scipy.stats.uniform(0, 180)},
    {"name": "sun_azimuth_angle", "datatype": float, "distribution": scipy.stats.uniform(0, 180)},
    {"name": "wetness", "datatype": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "wind_intensity", "datatype": float, "distribution": scipy.stats.uniform(0, 1)},
    {"name": "ego_vehicle", "datatype": Car, "distribution": EnumGen(Car)}
]

outputs = [
    {"name": "collisions_layout", "datatype": bool},
    # {"name": "collisions_pedestrian", "datatype": bool},
    {"name": "collisions_vehicle", "datatype": bool},
    {"name": "red_light", "datatype": bool, "distribution": scipy.stats.rv_discrete(name="red_light", values=(range(0, 2), [1/2]*2))},
    {"name": "vehicle_blocked", "datatype": bool, "distribution": scipy.stats.rv_discrete(name="vehicle_blocked", values=(range(0, 2), [1/2]*2))},
    {"name": "route_length", "datatype": float},
    {"name": "route_timeout", "datatype": bool},
    {"name": "score_route", "datatype": float},
    {"name": "score_composed", "datatype": float},
    {"name": "duration_game", "datatype": float},
    {"name": "duration_system", "datatype": float},
    # {"name": "status", "datatype": Status},
    # {"name": "stop_infraction", "datatype": int},
    # {"name": "total_steps", "datatype": int},
    {"name": "infraction", "datatype": Infraction, "distribution": EnumGen(Infraction)}
]


effects = {
    "NoEffect": NoEffect(),
    "SomeEffect": SomeEffect(),
    "Negative": Negative(),
    "Positive": Positive(),
    "1.0": ExactValue(1),
    "0.7": ExactValue(0.7),
    "0.65": ExactValue(0.65),
    "0.6": ExactValue(0.6)
}

# Create input structure required to create a modelling scenario
variables = [Input(i['name'], i['datatype'], i['distribution']) for i in inputs] + \
                   [Output(i['name'], i['datatype']) for i in outputs]

vnames = {v.name: v for v in variables}

constraints = [vnames["wind_intensity"].z3 <= 1,
vnames["wind_intensity"].z3 >= 0.3]

# Create modelling scenario to access z3 variable mirrors
modelling_scenario = Scenario(variables, constraints)
modelling_scenario.setup_treatment_variables()
print(modelling_scenario.variables)

class ScoreComposedEstimator(LinearRegressionEstimator):
    def __init__(
        self,
        treatment: tuple,
        treatment_values: float,
        control_values: float,
        adjustment_set: list[float],
        outcome: tuple,
        df: pd.DataFrame = None,
        effect_modifiers: dict[Variable:Any] = None,
        product_terms: list[tuple[Variable, Variable]] = None,
        intercept: int = 1,
    ):
        super().__init__(treatment=treatment,treatment_values=treatment_values,
        control_values=control_values,adjustment_set=adjustment_set,outcome=outcome, df=df,
        )
        self.add_product_term_to_df('score_route', 'red_light')
        self.add_product_term_to_df('score_route', 'collisions_vehicle')
        self.add_product_term_to_df('score_route', 'collisions_layout')
        # self.add_product_term_to_df('score_route', 'vehicle_blocked') # This shouldn't have a causal effect

def iv_estimator(**kwargs):
    return InstrumentalVariableEstimator(**kwargs, instrument="cloudiness")

estimators = {
    "LinearRegressionEstimator": LinearRegressionEstimator,
    "LogisticRegressionEstimator": LogisticRegressionEstimator,
    "ScoreComposedEstimator": ScoreComposedEstimator,
    "InfractionsEstimator": InfractionsEstimator,
    "InstrumentalVariableEstimator": iv_estimator
}

mutates = {
    "Increase": lambda x: modelling_scenario.treatment_variables[x].z3 >
                          modelling_scenario.variables[x].z3,
    "GoThrough": lambda x: And(modelling_scenario.treatment_variables[x].z3 == True, modelling_scenario.variables[x].z3 == False ),
    "Swap": lambda x: modelling_scenario.treatment_variables[x].z3 !=
                          modelling_scenario.variables[x].z3,
    "Plus1": lambda x: modelling_scenario.treatment_variables[x].z3 ==
                          modelling_scenario.variables[x].z3 + 1,
    "Plus5": lambda x: modelling_scenario.treatment_variables[x].z3 ==
                          modelling_scenario.variables[x].z3 + 5,
    "Plus10": lambda x: modelling_scenario.treatment_variables[x].z3 ==
                          modelling_scenario.variables[x].z3 + 10,
    "Plus20": lambda x: modelling_scenario.treatment_variables[x].z3 ==
                          modelling_scenario.variables[x].z3 + 20
}


if __name__ == "__main__":
    args = JsonUtility.get_args()
    json_utility = JsonUtility(args.log_path)  # Create an instance of the extended JsonUtility class
    json_utility.set_paths(args.json_path, args.dag_path, args.data_path)  # Set the path to the data.csv, dag.dot and causal_tests.json file

    # Load the Causal Variables into the JsonUtility class ready to be used in the tests
    json_utility.set_variables(inputs, outputs, [])
    json_utility.setup()  # Sets up all the necessary parts of the json_class needed to execute tests

    json_utility.generate_tests(effects, mutates, estimators, args.f)
