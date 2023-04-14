import numpy as np
import pandas as pd
import scipy
from enum import Enum
from typing import Any
from z3 import And
import statsmodels.api as sm

from causal_testing.specification.variable import Variable, Input, Output, Meta
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

Status = Enum("Status", ["Completed", "Failed", "Failed - Agent timed out"])

vehicles = {
    "vehicle.audi.a2": {
        "length": 1.852684736251831,
        "width": 0.8943394422531128,
        "height": 0.7735435366630554,
    },
    "vehicle.audi.tt": {
        "length": 2.0906050205230717,
        "width": 0.9970585703849792,
        "height": 0.6926480531692505,
    },
    "vehicle.bmw.grandtourer": {
        "length": 2.305502891540528,
        "width": 1.1208566427230835,
        "height": 0.8336379528045654,
    },
    "vehicle.yamaha.yzf": {
        "length": 1.1047229766845703,
        "width": 0.4335170984268188,
        "height": 0.6255727410316467,
    },
    "vehicle.audi.etron": {
        "length": 2.427854299545288,
        "width": 1.0163782835006714,
        "height": 0.8246796727180481,
    },
    "vehicle.nissan.micra": {
        "length": 1.8166879415512085,
        "width": 0.9225568771362304,
        "height": 0.750732421875,
    },
    "vehicle.bh.crossbike": {
        "length": 0.7436444163322449,
        "width": 0.4296287298202514,
        "height": 0.5397894978523254,
    },
    "vehicle.lincoln.mkz2017": {
        "length": 2.4508416652679443,
        "width": 1.0641621351242063,
        "height": 0.7553732395172119,
    },
    "vehicle.gazelle.omafiets": {
        "length": 0.9177202582359314,
        "width": 0.1644644439220428,
        "height": 0.5628286004066467,
    },
    "vehicle.tesla.cybertruck": {
        "length": 3.1367764472961426,
        "width": 1.1947870254516602,
        "height": 1.049095630645752,
    },
    "vehicle.dodge_charger.police": {
        "length": 2.487122058868408,
        "width": 1.0192006826400757,
        "height": 0.7771479487419128,
    },
    "vehicle.harley-davidson.low_rider": {
        "length": 1.1778701543807983,
        "width": 0.3818394243717193,
        "height": 0.6382853388786316,
    },
    "vehicle.bmw.isetta": {
        "length": 1.1036475896835327,
        "width": 0.7404598593711853,
        "height": 0.6893735527992249,
    },
    "vehicle.citroen.c3": {
        "length": 1.9938424825668333,
        "width": 0.9254241585731506,
        "height": 0.8085548281669617,
    },
    "vehicle.diamondback.century": {
        "length": 0.8214218020439148,
        "width": 0.1862581223249435,
        "height": 0.5119513869285583,
    },
    "vehicle.tesla.model3": {
        "length": 2.3958897590637207,
        "width": 1.081725001335144,
        "height": 0.744159996509552,
    },
    "vehicle.seat.leon": {
        "length": 2.0964150428771973,
        "width": 0.9080929160118104,
        "height": 0.7369155883789062,
    },
    "vehicle.kawasaki.ninja": {
        "length": 1.0166761875152588,
        "width": 0.4012899398803711,
        "height": 0.5727267861366272,
    },
    "vehicle.nissan.patrol": {
        "length": 2.3022549152374268,
        "width": 0.9657965898513794,
        "height": 0.927423059940338,
    },
    "vehicle.mercedes-benz.coupe": {
        "length": 2.513388395309448,
        "width": 1.0757731199264526,
        "height": 0.8177640438079834,
    },
    "vehicle.jeep.wrangler_rubicon": {
        "length": 1.933110356330872,
        "width": 0.95259827375412,
        "height": 0.9389679431915284,
    },
    "vehicle.mustang.mustang": {
        "length": 2.358762502670288,
        "width": 0.947413444519043,
        "height": 0.650469958782196,
    },
    "vehicle.volkswagen.t2": {
        "length": 2.2402184009552,
        "width": 1.034657597541809,
        "height": 1.0188955068588257,
    },
    "vehicle.chevrolet.impala": {
        "length": 2.6787397861480717,
        "width": 1.0166015625,
        "height": 0.7053292393684387,
    },
    "vehicle.carlamotors.carlacola": {
        "length": 2.601919174194336,
        "width": 1.3072861433029177,
        "height": 1.2337223291397097,
    },
}


class InfractionsEstimator(Estimator):
    def add_modelling_assumptions(self):
        self.modelling_assumptions += (
            "The variables in the data must fit a shape which can be expressed as a linear"
            "combination of parameters and functions of variables. Note that these functions"
            "do not need to be linear."
        )

    def estimate_ate(self):
        stratum = self.df.where(
            self.df["infraction"] == self.effect_modifiers["infraction"]
        ).dropna()
        model = sm.OLS(stratum["score_composed"], stratum[["score_route"]]).fit()
        return model.params["score_route"], sorted(
            model.conf_int(alpha=0.05, cols=None).loc["score_route"]
        )


class Car(Enum):
    a2 = "vehicle.audi.a2"
    etron = "vehicle.audi.etron"
    tt = "vehicle.audi.tt"
    crossbike = "vehicle.bh.crossbike"
    grandtourer = "vehicle.bmw.grandtourer"
    isetta = "vehicle.bmw.isetta"
    carlacola = "vehicle.carlamotors.carlacola"
    impala = "vehicle.chevrolet.impala"
    c3 = "vehicle.citroen.c3"
    century = "vehicle.diamondback.century"
    police = "vehicle.dodge_charger.police"
    omafiets = "vehicle.gazelle.omafiets"
    low_rider = "vehicle.harley-davidson.low_rider"
    wrangler_rubicon = "vehicle.jeep.wrangler_rubicon"
    ninja = "vehicle.kawasaki.ninja"
    mkz2017 = "vehicle.lincoln.mkz2017"
    coupe = "vehicle.mercedes-benz.coupe"
    cooperst = "vehicle.mini.cooperst"
    mustang = "vehicle.mustang.mustang"
    micra = "vehicle.nissan.micra"
    patrol = "vehicle.nissan.patrol"
    leon = "vehicle.seat.leon"
    cybertruck = "vehicle.tesla.cybertruck"
    model3 = "vehicle.tesla.model3"
    prius = "vehicle.toyota.prius"
    t2 = "vehicle.volkswagen.t2"
    yzf = "vehicle.yamaha.yzf"

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented


class EnumGen(scipy.stats.rv_discrete):
    def __init__(self, dt: Enum):
        self.dt = dict(enumerate(dt, 1))
        self.inverse_dt = {v: k for k, v in self.dt.items()}

    def ppf(self, q, *args, **kwds):
        return np.vectorize(self.dt.get)(np.ceil(len(self.dt) * q))

    def cdf(self, q, *args, **kwds):
        return np.vectorize(self.inverse_dt.get)(q) / len(Car)


class Infraction(Enum):
    red_light = "red_light"
    # collisions_pedestrian = 'collisions_pedestrian'
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


inputs = [
    {
        "hidden": True,
        "name": "percentage_speed_limit",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 100),
    },
    {
        "name": "cloudiness",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 100),
    },
    {
        "name": "fog_density",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 100),
    },
    {
        "name": "fog_distance",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 100),
    },
    {
        "name": "fog_falloff",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 100),
    },
    {
        "hidden": True,
        "name": "number_of_drivers",
        "datatype": int,
        "distribution": scipy.stats.rv_discrete(
            name="drivers", values=(range(0, 200), [1 / 200] * 200)
        ),
    },
    {
        "hidden": True,
        "name": "number_of_walkers",
        "datatype": int,
        "distribution": scipy.stats.rv_discrete(
            name="drivers", values=(range(0, 200), [1 / 200] * 200)
        ),
    },
    {
        "name": "precipitation",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 100),
    },
    {
        "name": "precipitation_deposits",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 100),
    },
    {
        "name": "sun_altitude_angle",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 180),
    },
    {
        "name": "sun_azimuth_angle",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 180),
    },
    {"name": "wetness", "datatype": float, "distribution": scipy.stats.uniform(0, 100)},
    {
        "name": "wind_intensity",
        "datatype": float,
        "distribution": scipy.stats.uniform(0, 1),
    },
    {"name": "ego_vehicle", "datatype": Car, "distribution": EnumGen(Car)},
]

outputs = [
    {"name": "score_penalty", "datatype": float},
    {"name": "route_length", "datatype": float},
    {"name": "route_timeout", "datatype": bool},
    {"name": "score_route", "datatype": float},
    {"name": "score_composed", "datatype": float},
    {"name": "duration_game", "datatype": float},
    {"name": "duration_system", "datatype": float},
    {"name": "infraction", "datatype": Infraction, "distribution": EnumGen(Infraction)},
]

def populate_ego_vehicle_dim(dim, data):
    data[f'ego_vehicle_{dim}'] = np.vectorize(lambda v: vehicles.get(v, None))(data['ego_vehicle'])
    data[f'ego_vehicle_{dim}'] = np.vectorize(lambda v: v[dim] if v else None)(data[f'ego_vehicle_{dim}'])

def populate_infraction_occurred(data):
    infractions = [c for c in data.columns if "collisions" in c] + [
        "red_light",
        "stop_infraction",
    ]
    data["infraction_occurred"] = data[infractions].any(axis=1).astype(int)

metas = [
    {"name": "ego_vehicle_length", "datatype": float, "populate": lambda data: populate_ego_vehicle_dim("length", data)},
    {"name": "ego_vehicle_width", "datatype": float, "populate": lambda data: populate_ego_vehicle_dim("width", data)},
    {"name": "ego_vehicle_height", "datatype": float, "populate": lambda data: populate_ego_vehicle_dim("height", data)},
    {"name": "infraction_occurred", "datatype": int, "populate": populate_infraction_occurred},
]


effects = {
    "NoEffect": NoEffect(),
    "SomeEffect": SomeEffect(),
    "Negative": Negative(),
    "Positive": Positive(),
    "1.0": ExactValue(1),
    "0.8": ExactValue(0.8),
    "0.7": ExactValue(0.7),
    "0.65": ExactValue(0.65),
    "0.6": ExactValue(0.6),
    "0.5": ExactValue(0.5),
}

# Create input structure required to create a modelling scenario
variables = ([Input(i["name"], i["datatype"], i["distribution"]) for i in inputs] +
[    Output(i["name"], i["datatype"]) for i in outputs] +
[    Meta(i["name"], i["datatype"], i["populate"]) for i in metas])


vnames = {v.name: v for v in variables}

constraints = [vnames["wind_intensity"].z3 <= 1, vnames["wind_intensity"].z3 >= 0.3]

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
        super().__init__(
            treatment=treatment,
            treatment_values=treatment_values,
            control_values=control_values,
            adjustment_set=adjustment_set,
            outcome=outcome,
            df=df,
        )
        self.add_product_term_to_df("score_route", "red_light")
        self.add_product_term_to_df("score_route", "collisions_vehicle")
        self.add_product_term_to_df("score_route", "collisions_layout")
        # self.add_product_term_to_df('score_route', 'vehicle_blocked') # This shouldn't have a causal effect


def iv_estimator(**kwargs):
    return InstrumentalVariableEstimator(**kwargs, instrument="cloudiness")


estimators = {
    "LinearRegressionEstimator": LinearRegressionEstimator,
    "LogisticRegressionEstimator": LogisticRegressionEstimator,
    "ScoreComposedEstimator": ScoreComposedEstimator,
    "InfractionsEstimator": InfractionsEstimator,
    "InstrumentalVariableEstimator": iv_estimator,
}

mutates = {
    "Increase": lambda x: modelling_scenario.treatment_variables[x].z3
    > modelling_scenario.variables[x].z3,
    "GoThrough": lambda x: And(
        modelling_scenario.treatment_variables[x].z3 == True,
        modelling_scenario.variables[x].z3 == False,
    ),
    "Swap": lambda x: modelling_scenario.treatment_variables[x].z3
    != modelling_scenario.variables[x].z3,
    "Plus1": lambda x: modelling_scenario.treatment_variables[x].z3
    == modelling_scenario.variables[x].z3 + 1,
    "Plus5": lambda x: modelling_scenario.treatment_variables[x].z3
    == modelling_scenario.variables[x].z3 + 5,
    "Plus10": lambda x: modelling_scenario.treatment_variables[x].z3
    == modelling_scenario.variables[x].z3 + 10,
    "Plus20": lambda x: modelling_scenario.treatment_variables[x].z3
    == modelling_scenario.variables[x].z3 + 20,
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
    json_utility.set_variables(inputs, outputs, metas)
    json_utility.setup()  # Sets up all the necessary parts of the json_class needed to execute tests

    json_utility.generate_tests(effects, mutates, estimators, args.f)
