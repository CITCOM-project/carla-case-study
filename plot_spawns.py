#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 13:55:36 2023

@author: michael
"""

import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import json
import os
from scipy.spatial import distance
from PIL import Image
import urllib.request
import io

interfuser_routes = ET.parse(
    "InterFuser/leaderboard/data/training_routes/routes_town01_short.xml"
).getroot()
tcp_routes = ET.parse(
    "TCP/leaderboard/data/TCP_training_routes/routes_town01.xml"
).getroot()

interfuser_results_dir = "InterFuser/collected_data/dataset/weather-0/data"

TRAFFIC_LIGHTS = [
    (94.989975, 70.409996, 0.103242),
    (102.720001, 52.850018, 0.103262),
    (85.729996, 45.779999, 0.104207),
    (94.989967, 144.380020, 0.103242),
    (102.719986, 126.820015, 0.103262),
    (85.729988, 119.750000, 0.104207),
    (94.989967, 209.919998, 0.103242),
    (102.719986, 192.550003, 0.103262),
    (85.729988, 185.289993, 0.104207),
    (106.119980, 324.080017, 0.103242),
    (85.629936, 316.350067, 0.103262),
    (75.710014, 333.339996, 0.104207),
    (349.600006, 324.080078, 0.103242),
    (332.039948, 316.350098, 0.103262),
    (324.970001, 333.339966, 0.104207),
    (168.869995, 53.030037, 0.103242),
    (151.309952, 45.300076, 0.103262),
    (144.240036, 62.289997, 0.104207),
    (331.990021, 44.880039, 0.103242),
    (321.760101, 62.440075, 0.103262),
    (341.359985, 12.710039, 0.103262),
    (348.429993, -4.479961, 0.104207),
    (341.250031, 69.509956, 0.104207),
    (331.990021, 118.930038, 0.103242),
    (321.680115, 136.132156, 0.103262),
    (341.250031, 143.559952, 0.104207),
    (331.990021, 184.470032, 0.103242),
    (323.410095, 202.030075, 0.103262),
    (341.250031, 209.099960, 0.104207),
    (143.119995, 4.830009, 0.103242),
    (160.679993, 12.559999, 0.103262),
    (167.750000, -4.429990, 0.104207),
    (77.479996, 4.830000, 0.103242),
    (95.040001, 12.560010, 0.103262),
    (102.110001, -4.429990, 0.104207),
    (323.799988, 4.980000, 0.103242),
]


def get_routes(routes):
    X = []
    Y = []
    for route in routes:
        if route[0].tag == "weather":
            route = route[0]
        X.append(float(route[0].attrib["x"]))
        # Flip Y to convert between coordinate systems
        Y.append(-float(route[0].attrib["y"]))
    return X, Y


def closest_node(node, nodes):
    closest_index = distance.cdist([node], nodes).argmin()
    return nodes[closest_index]


fig, ax = plt.subplots(1, 1, figsize=(10, 10))

URL = "https://carla.readthedocs.io/en/0.9.10/img/Town01.jpg"
with urllib.request.urlopen(URL) as url:
    f = io.BytesIO(url.read())
    img = Image.open(f)


offset_x = -15
offset_y = -370
size = 425
ax.imshow(
    img, extent=[0 + offset_x, size + offset_x, 0 + offset_y, size + offset_y - 5]
)

X, Y = get_routes(interfuser_routes)
ax.scatter(X, Y, color="darkcyan")

spawns = {}

for i, (x, y) in enumerate(zip(X, Y)):
    if (x, y) not in spawns:
        spawns[(x, y)] = []
    spawns[(x, y)].append(str(i))
for x, y in spawns:
    ax.annotate(", ".join(spawns[(x, y)]), (x + 5, y), color="cyan")

actual_X = []
actual_Y = []
for route in os.listdir(interfuser_results_dir):
    with open(f"{interfuser_results_dir}/{route}/measurements/0000.json") as f:
        data = json.load(f)
        actual_X.append(data["x"])
        actual_Y.append(-data["y"])

for x, y in zip(X, Y):
    print(closest_node((x, y), list(zip(actual_X, actual_Y))))
    x_, y_ = closest_node((x, y), list(zip(actual_X, actual_Y)))
    xx = [x, x_]
    yy = [y, y_]
    plt.plot(xx, yy, color="darkcyan")
ax.scatter(actual_X, actual_Y, color="cyan", zorder=10)

X, Y = get_routes(tcp_routes)
ax.scatter(X, Y, color="orange")

X, Y, _ = zip(*TRAFFIC_LIGHTS)
ax.scatter(X, [-y for y in Y], color="lime")

ax.set_facecolor("#535550")

plt.show()
