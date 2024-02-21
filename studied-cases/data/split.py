import pandas as pd

for ads in ["garage", "TCP"]:
    for driver in ["privileged", "trained"]:
        df = pd.read_csv(f"{ads}_{driver}_data.csv", index_col=0)
        count = {}
        for i in df.route_id:
            if i not in count:
                count[i] = 0
            count[i] += 1
        assert all(count[i] == 4 for i in count)
        carla_10 = df.query("carla_version == 10").sort_values(["ego_vehicle", "route_id"]).reset_index()
        carla_11 = df.query("carla_version == 11").sort_values(["ego_vehicle", "route_id"]).reset_index()
        assert len(carla_10) % 4 == 0 and len(carla_10) == len(carla_11)
        quarter = int(len(carla_10) / 4)
        carla_10 = carla_10.iloc[quarter : (len(carla_10) - quarter)]
        carla_11 = carla_11.iloc[quarter : (len(carla_11) - quarter)]

        for i in carla_10.route_id:
            count[i] = 1
        assert all(count[i] == 1 for i in count)
        for i in carla_11.route_id:
            count[i] = 1
        assert all(count[i] == 1 for i in count)

        pd.concat([carla_10, carla_11]).to_csv(f"{ads}_{driver}_half.csv")
