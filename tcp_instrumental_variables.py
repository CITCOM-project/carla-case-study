#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:34:58 2023

@author: michael
"""

import pandas as pd
import statsmodels.api as sm

v1_datapath = "data/TCP.csv"
v2_datapath = "data/TCP_original.csv"
inputs = [
    "cloudiness",
    #  No fog in the runs
    # "fog_density",
    # "fog_distance",
    # "fog_falloff",
    "precipitation",
    "precipitation_deposits",
    "sun_altitude_angle",
    "sun_azimuth_angle",
    # "wetness",
    "wind_intensity",
    # "ego_vehicle",
    # "ego_vehicle_color",
    # "ego_vehicle_number_of_wheels",
    # "ego_vehicle_object_type",
    # "ego_vehicle_role_name",
    # "ego_vehicle_sticky_control",
    # "number_of_drivers", # Can't use as an instrument
    # "number_of_walkers", # Can't use as an instrument
    # "percentage_speed_limit",
    "route_length",
]


def calculate_coefficients(df_original, df_modified):
    total_effect_modified = sm.OLS(
        df_modified["duration_system"], df_modified[[ip, "Intercept"]]
    ).fit()
    total_effect_original = sm.OLS(
        df_original["duration_system"], df_original[[ip, "Intercept"]]
    ).fit()

    # calculate ip -> game time
    direct_effect_modified = sm.OLS(
        df_modified["duration_game"], df_modified[[ip, "Intercept"]]
    ).fit()
    direct_effect_original = sm.OLS(
        df_original["duration_game"], df_original[[ip, "Intercept"]]
    ).fit()

    return (total_effect_original.params[ip] / direct_effect_original.params[ip],
        total_effect_modified.params[ip] / direct_effect_modified.params[ip])

df_modified = pd.read_csv(v1_datapath, index_col=0)
df_modified["Intercept"] = 1
df_original = pd.read_csv(v2_datapath, index_col=0)
df_original["Intercept"] = 1
df_original["number_of_drivers"] = 120
df_original["number_of_walkers"] = 0

# using df_modified[[ip]] to calculate direct_effect_original is NOT a bug because the
# routes have the same weather conditions
for ip in inputs:
    df_original[ip] = df_modified[ip]

data = {}
BOOTSTRAPS = 100

# Try each input as an instrument
for ip in inputs:
    print(ip, len(set(df_modified[ip])))
    effect_original, effect_modified = calculate_coefficients(df_original, df_modified)

    bootstrap_samples = [
                calculate_coefficients(df_original.sample(len(df_original), replace=True), df_modified.sample(len(df_modified), replace=True))
                for _ in range(BOOTSTRAPS)
            ]
    original, modified = zip(*bootstrap_samples)

    original = sorted(list(original))
    modified = sorted(list(modified))

    bound = int((BOOTSTRAPS * 0.05) / 2)
    modified_low = modified[bound]
    modified_high = modified[BOOTSTRAPS - bound]
    original_low = original[bound]
    original_high = original[BOOTSTRAPS - bound]

    data[ip.replace("_", "\_")] = {
        "datapoints": len(set(df_modified[ip])),
        "effect modified": str(round(effect_modified, 2)),
        "modified low": str(round(modified_low, 2)),
        "modified high": str(round(modified_high, 2)),
        "effect original": str(round(effect_original, 2)),
        "original low": str(round(original_low, 2)),
        "original high": str(round(original_high, 2)),
    }


adjusted_modified = sm.OLS(
    df_modified["duration_system"],
    df_modified[
        [
            "duration_game",
            "number_of_drivers",
            "number_of_walkers",
            "Intercept",
        ]
    ],
).fit()
adjusted_original = sm.OLS(
    df_original["duration_system"],
    df_original[
        [
            "duration_game",
            "number_of_drivers",
            "number_of_walkers",
            "Intercept",
        ]
    ],
).fit()


data["Classical adjustment"] = {
    "datapoints": None,
    "effect modified": str(round(adjusted_modified.params['duration_game'], 2)),
    "modified low": str(adjusted_modified.conf_int().loc['duration_game'].round(2)[0]),
    "modified high": str(adjusted_modified.conf_int().loc['duration_game'].round(2)[1]),
    "effect original": str(round(adjusted_original.params['duration_game'], 2)),
    "original low": str(adjusted_original.conf_int().loc['duration_game'].round(2)[0]),
    "original high": str(adjusted_original.conf_int().loc['duration_game'].round(2)[1]),
}



data = (
    pd.DataFrame(data)
    .transpose()
)
data["effect modified"] = data['effect modified'].astype(float)
print(data)
data["effect_modified"] = [f"{row['effect modified']}[{row['modified low']},{row['modified high']}]" for _, row in data.iterrows()]
data["effect_original"] = [f"{row['effect original']}[{row['original low']},{row['original high']}]" for _, row in data.iterrows()]
print(data[['datapoints','effect_modified','effect_original']].style.to_latex())
