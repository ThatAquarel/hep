import glob
from io import StringIO
from datetime import timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# TODO: Add docstrings to all functions and classes
# TODO: Add the folowing functions:
#       - avg_angle_of_incidence
#       - avg_trajectory
#       - basic_avg_analysis
#       - hps_plot


class AnalysisTool:
    def __init__ (self, data):
        match type(data):
            case str():
                self.data = self.parse_data(data)
            case pd.DataFrame():
                self.data = data

    
    def parse_data(data_dir : str) -> pd.DataFrame:
        UNIX_TIME, DATE_TIME, N = "unix_time", "time", "n"  

        log_files = glob.glob(data_dir)

        trigger_data = []

        for log_file in log_files:
            with open(log_file, "r") as handle:
                lines = np.array(handle.readlines())
                lines = lines[lines != "start recorder\n"]
                lines = lines[~np.strings.startswith(lines, "restart")]

                trigger_data.append(lines[::4])

        n_triggers = sum([len(i) for i in trigger_data])
        flattened = np.empty(shape=n_triggers, dtype=trigger_data[0].dtype)
        i = 0
        for data in trigger_data:
            flattened[i : i + len(data)] = data
            i += len(data)

        str_io = StringIO("".join(flattened))
        df = pd.read_csv(str_io, header=None, names=[UNIX_TIME, N])
        df[DATE_TIME] = pd.to_datetime(df[UNIX_TIME], unit="s", utc=True).dt.tz_convert(
            "America/Toronto"
        )
        df = df.sort_values(by=UNIX_TIME)

        return df