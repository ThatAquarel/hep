import glob

from io import StringIO

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def parse_data(directory):
    files = glob.glob(directory)

    lines = []
    for file in files:
        with open(file, "r") as f:
            lines.extend(f.readlines())

    # data_str = "".join(lines)
    str_io = StringIO("".join(lines))
    df = pd.read_csv(str_io, header=None, names=["unix", "humidity", "temp"])

    df["time"] = pd.to_datetime(df["unix"], unit="s", utc=True).dt.tz_convert(
        "America/Toronto"
    )
    df = df.sort_values(by="unix")

    return df



def main():
    df = parse_data("scintillator_field/data/11_incline_west/sc_temp*")


    ...



if __name__ == "__main__":
    main()
