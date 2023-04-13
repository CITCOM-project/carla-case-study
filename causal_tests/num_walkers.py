#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 13:52:57 2023

@author: michael
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

df = pd.read_csv("../data/big_data.csv")
plt.scatter(df["number_of_walkers"], df["red_light"])

mod = sm.OLS(df["number_of_walkers"], df["red_light"]).fit()
print(mod.summary())
