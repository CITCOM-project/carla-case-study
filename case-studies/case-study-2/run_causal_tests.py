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


inputs = [
    {
        "name": "percentage_speed_limit",
        "datatype": float,
    },
    {
        "name": "cloudiness",
        "datatype": float,
    },
    {
        "name": "number_of_drivers",
        "datatype": int,
    },
    {
        "name": "number_of_walkers",
        "datatype": int,
    },
    {
        "name": "precipitation",
        "datatype": float,
    },
    {
        "name": "precipitation_deposits",
        "datatype": float,
    },
    {
        "name": "sun_altitude_angle",
        "datatype": float,
    },
    {
        "name": "sun_azimuth_angle",
        "datatype": float,
    },
    {
        "name": "wind_intensity",
        "datatype": float,
    },
    {"name": "ego_vehicle", "datatype": Car},
    {"name": "route_length", "datatype": float},
]

outputs = [
    {"name": "score_penalty", "datatype": float},
    {"name": "duration_game", "datatype": float},
    {"name": "duration_system", "datatype": float},
]


def populate_ego_vehicle_dim(dim, data):
    data[f"ego_vehicle_{dim}"] = np.vectorize(lambda v: vehicles.get(v, None))(
        data["ego_vehicle"]
    )
    data[f"ego_vehicle_{dim}"] = np.vectorize(lambda v: v[dim] if v else None)(
        data[f"ego_vehicle_{dim}"]
    )


def populate_infraction_occurred(data):
    infractions = [c for c in data.columns if "collisions" in c] + [
        "red_light",
        "stop_infraction",
    ]
    data["infraction_occurred"] = data[infractions].any(axis=1).astype(int)


metas = [
    {
        "name": "ego_vehicle_length",
        "datatype": float,
        "populate": lambda data: populate_ego_vehicle_dim("length", data),
    },
    {
        "name": "ego_vehicle_width",
        "datatype": float,
        "populate": lambda data: populate_ego_vehicle_dim("width", data),
    },
    {
        "name": "ego_vehicle_height",
        "datatype": float,
        "populate": lambda data: populate_ego_vehicle_dim("height", data),
    },
    {
        "name": "infraction_occurred",
        "datatype": int,
        "populate": populate_infraction_occurred,
    },
]


effects = {
    "NoEffect": NoEffect(),
    "SomeEffect": SomeEffect(),
}

# Create input structure required to create a modelling scenario
variables = (
    [Input(i["name"], i["datatype"]) for i in inputs]
    + [Output(i["name"], i["datatype"]) for i in outputs]
    + [Meta(i["name"], i["datatype"], i["populate"]) for i in metas]
)


# Create modelling scenario to access z3 variable mirrors

modelling_scenario = Scenario(variables, constraints=[])
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

    json_utility.run_json_tests(
        effects, mutates={}, estimators=estimators, f_flag=args.f
    )
