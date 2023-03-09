#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 15:24:58 2023

@author: michael
"""

import pandas as pd
from enum import Enum
import sys

DATAPATH = sys.argv[1]

df = pd.read_csv(DATAPATH)

infractions = [x for x in df.columns if "collisions" in x] + ["red_light", "stop_infraction"]
Infraction = Enum("Infraction", infractions)
df['infraction'] = False

for i in infractions:
    df['infraction'] = [i if x else infraction for infraction, x in zip(df['infraction'], df[i])]

df.to_csv(DATAPATH.replace(".csv", "_infractions.csv"))
