import numpy as np
import pandas as pd
from lifelines.utils import concordance_index


def score(solution: pd.DataFrame, submission: pd.DataFrame, row_id_column_name: str) -> float:
    del solution[row_id_column_name]
    del submission[row_id_column_name]

    event_label = "efs"
    interval_label = "efs_time"
    prediction_label = "prediction"

    merged_df = pd.concat([solution, submission], axis=1)
    merged_df_race_dict = dict(merged_df.groupby(["race_group"]).groups)
    metric_list = []

    for race in merged_df_race_dict.keys():
        indices = sorted(merged_df_race_dict[race])
        merged_df_race = merged_df.iloc[indices]
        c_index_race = concordance_index(
            merged_df_race[interval_label], -merged_df_race[prediction_label], merged_df_race[event_label]
        )
        metric_list.append(c_index_race)

    return float(np.mean(metric_list) - np.sqrt(np.var(metric_list)))
