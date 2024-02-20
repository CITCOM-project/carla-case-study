#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 14:15:35 2024

@author: michael
"""

import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

infraction_name = "collisions_layout"

def check_driver(driver):
    print(driver)
    df = pd.read_csv(f"data/{driver}_trained_data.csv").query(f"infraction_name == '{infraction_name}'")
    model = smf.ols("driving_score ~ completion_score", df).fit()
    plt.scatter(df["completion_score"], df["driving_score"])
    plt.plot(df["completion_score"], model.predict(df["completion_score"]), label=driver)
    print(model.params)
    print(df["outside_route_lanes"])
    print()

check_driver("TCP")
check_driver("garage")

plt.legend()
