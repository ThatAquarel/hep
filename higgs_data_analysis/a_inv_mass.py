# Invariant Mass Calculator
#
# Computes masses for diphoton events
#
# Requirements:
#    numpy
#    pandas
#
# Command line arguemnts:
#    -i input.dat
#    -o output.csv
#
# Example:
#    python a_inv_mass.py -i TenEvents.dat -o mass.csv
#    python a_inv_mass.py -i studentsDataA/DiphotonsA.dat -o inv_mass_a.csv
#
# 2024/11/08   Alex Xia: Initial Code


import argparse
from itertools import combinations

import numpy as np
import pandas as pd


def main(events_file, mass_file):
    with open(events_file, "r") as f:
        header_rows = []
        for i, l in enumerate(f):
            if l.startswith("#"):
                header_rows.append(i)
            if len(header_rows) and (i - header_rows[-1]) > 5:
                break
    events = pd.read_csv(events_file, sep="\\s+", skiprows=header_rows)
    (event_start,) = np.where(events["#"] == 0)

    event_col = np.empty(len(events), dtype=np.int32)
    for i, start in enumerate(event_start):
        try:
            end = event_start[i + 1]
        except IndexError:
            end = len(event_col)

        event_col[start:end] = i

    event_col = pd.Series(event_col, name="event_n", copy=False)
    events = pd.concat([event_col, events], axis=1)

    y = events[events["typ"] == 0]
    n_y_max = y["#"].max()
    print(f"max {n_y_max} photons per event")
    n_events = len(event_start)
    print(f"calculate inv mass for {n_events} events")

    y_groups = []
    indices = pd.Series(range(n_events), name="event_n")
    for i in range(1, n_y_max + 1):
        y_g = y[y["#"] == i].set_index("event_n")

        group = pd.DataFrame(index=indices, columns=["eta", "phi", "pt"])
        group[["eta", "phi", "pt"]] = y_g[["eta", "phi", "pt"]]

        y_groups.append(group)

    y_combinations = combinations(range(n_y_max), 2)

    mass_col = lambda i, j: f"M{i}{j}"
    columns = [mass_col(i, j) for i, j in y_combinations]
    columns.insert(0, "photons")

    mass = pd.DataFrame(index=indices, columns=columns)
    mass["photons"] = np.bincount(y["event_n"])

    for i, j in combinations(range(n_y_max), 2):
        y_a, y_b = y_groups[i], y_groups[j]

        cosh_d_eta = np.cosh(y_a["eta"] - y_b["eta"])
        cos_d_phi = np.cos(y_a["phi"] - y_b["phi"])

        m = np.sqrt(2 * np.abs(y_a["pt"] * y_b["pt"]) * (cosh_d_eta - cos_d_phi))
        mass[mass_col(i, j)] = m

    mass.to_csv(mass_file, index=True, index_label="event")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Invariant Mass Calculator")
    parser.add_argument("-i", "--input", default="TenEvents.dat")
    parser.add_argument("-o", "--output", default="TenEvents.dat_inv_mass.csv")

    args = parser.parse_args()

    main(args.input, args.output)
