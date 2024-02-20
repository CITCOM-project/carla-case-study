import json
import pandas as pd
from glob import glob
from pathlib import Path

infractions = {
    "no_infraction": 1,
    "red_light": 0.7,
    "collisions_layout": 0.65,
    "collisions_vehicle": 0.6,
    "collisions_pedestrian": 0.5,
}


df = {}


def format(key):
    return "-" if pd.isnull(test[key]) else f"{test[key]:.3f}"


def highlight(outcome):
    return "\red{" + outcome + "}"


for file in glob("results/*.json"):
    with open(file) as f:
        tests = json.load(f)
    file = Path(file).stem.replace("_results", "").replace("_", " ")
    for test in tests:
        test_name = test["name"]
        infraction_name = "_".join(test_name.split("_")[:2])
        if test_name not in df:
            df[test_name] = {
                "Infraction": " ".join(infraction_name.capitalize().split("_")),
                "Expected": infractions[infraction_name],
            }
        if "result" not in test:
            df[test_name][file] = highlight("-")
            continue
        for k, v in test.pop("result").items():
            test[k] = v
        outcome = f"{format('effect_estimate')}[{format('ci_low')}, {format('ci_high')}]"
        df[test_name][file] = highlight(outcome) if test["failed"] else outcome


df = pd.DataFrame(df.values())
df.to_latex("results/all_results.tex", escape=False, index=False)
