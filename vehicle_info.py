#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 13:51:45 2023

@author: michael
"""
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np


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

inputs = [
    # "cloudiness",
    # "fog_density",
    # "fog_distance",
    # "fog_falloff",
    # "precipitation",
    # "precipitation_deposits",
    # "sun_altitude_angle",
    # "sun_azimuth_angle",
    # "wetness",
    # "wind_intensity",
    # "ego_vehicle",
    # "ego_vehicle_color",
    # "ego_vehicle_number_of_wheels",
    # "ego_vehicle_object_type",
    # "ego_vehicle_role_name",
    # "ego_vehicle_sticky_control",
    "number_of_drivers",
    "number_of_walkers",
    "percentage_speed_limit",
    "route_length",
    # "total_steps",
    # "score_composed",
    # "score_penalty",
    # "score_route",
    # "ego_vehicle_driver_id",
    # "crashed_out_early",
]

data = pd.read_csv("TCP/data/TCP_random_vehicle.csv", index_col=0)
data["crashed_out_early"] = (data["duration_game"] < 1).astype(int)
print(data.columns)

for dim in ["length", "width", "height"]:
    data[f"ego_vehicle_{dim}"] = [
        vehicles[v][dim] if v in vehicles else None for v in data["ego_vehicle"]
    ]

infractions = [c for c in data.columns if "collisions" in c] + [
    "red_light",
    "stop_infraction",
]
data["infraction_committed"] = data[infractions].any(axis=1).astype(int)

length_infractions = []
for length, g in data[["ego_vehicle_length", "red_light"]].groupby(
    "ego_vehicle_length"
):
    length_infractions.append((length, g.sum()["red_light"] / len(g)))

# plt.scatter(data['ego_vehicle_width'], data['red_light'])

# train = (
#     data[inputs+["red_light", "ego_vehicle_length", "ego_vehicle_width", "crashed_out_early"]]
#     .where(data["ego_vehicle_length"] < 3)
#     .where(1 < data["ego_vehicle_length"])
#     .dropna()
# )
# train["Intercept"] = 1
# # model = sm.Logit(train['red_light'], train[['ego_vehicle_length', 'Intercept']]).fit()
# model = sm.OLS(train["red_light"], train[["ego_vehicle_length", "route_length", "number_of_walkers", "number_of_drivers"]]).fit()
# # print(model.summary())

# coefs = pd.DataFrame(
#     {
#         "coef": model.params.values,
#         "odds ratio": np.exp(model.params.values),
#     },
#     index=model.params.index,
# )
# print(coefs)

# X = pd.DataFrame()
# X['ego_vehicle_length'] = np.linspace(0.5, 3, 11)
# X['intercept'] = 1
# X['odds(red_light)'] = model.predict(X)
# # print(X)
# plt.plot(X['ego_vehicle_length'], X['odds(red_light)'])

# plt.scatter(train["ego_vehicle_length"], train["red_light"])

# plt.hist(train['ego_vehicle_length'])
# x, y = zip(*length_infractions)
# model = sm.OLS(y, x).fit()
# # print(model.summary())
# plt.scatter(x,y)
# plt.xlabel("Length")
# plt.ylabel("P(Red Light Infraction)")

outcome = "duration_game"
for col in data:
    if col in [outcome, "infraction_committed"] + inputs or data.dtypes[col] not in [
        int,
        float,
    ]:
        continue
    train = data[[col, outcome, "infraction_committed"] + inputs].dropna()
    if len(train) == 0:
        continue
    train["intercept"] = 1
    # train = train.where(data['red_light'] == 1).dropna()
    model = sm.OLS(
        train[outcome], train[[col, "infraction_committed", "route_length", "number_of_walkers", "number_of_drivers", "intercept"] + inputs]
    ).fit()
    if not model.conf_int().loc[col][0] <= 0 <= model.conf_int().loc[col][1]:
        print(col)
        print(
            model.conf_int().loc[col][0],
            model.params[col],
            model.conf_int().loc[col][1],
        )
        print()
