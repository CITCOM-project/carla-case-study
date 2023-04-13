#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 10:32:02 2023

@author: michael
"""
import pandas as pd
import statsmodels.api as sm
import numpy as np

df = pd.read_csv("../new_data/big_data.csv")
exog = df[["ego_vehicle"]]

endog = df["collisions_vehicle"]


exog = sm.add_constant(exog, prepend=False)
exog = pd.get_dummies(exog, columns=["ego_vehicle"], drop_first=True)

model = sm.OLS(endog, exog).fit()

print(model.summary())
