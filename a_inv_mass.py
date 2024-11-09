# Invariant Mass Calculator
#    Computes masses for diphoton events
#    https://github.com/ThatAquarel/hep
#
# Requirements:
#    numpy
#    pandas
#
# Example:
#    With events file TenEvents.dat, ouput invariant masses as mass.csv:
#    >> python a_inv_mass.py -i TenEvents.dat -o mass.csv
#
#    With events file DiphotonsA.dat, ouput invariant masses as inv_mass_a.csv:
#    >> python a_inv_mass.py -i studentsDataA/DiphotonsA.dat -o inv_mass_a.csv
#
# Modifications:
#    2024/11/08   Alex Xia:     Initial Code, Author
#

import argparse
from itertools import combinations

import numpy as np
import pandas as pd


def main(
    events_file,
    mass_file,
):
    """
    Computes masses for diphoton events

    :param events_file:     Input events file in .dat format
    :param mass_file:       Output calculated masses in .csv
    """

    # identify rows of header
    with open(events_file, "r") as f:
        header_rows = []
        for i, l in enumerate(f):
            # accumulate rows that start
            # with a hashtag (header)
            if l.startswith("#"):
                header_rows.append(i)

            # optimization: break out of
            # loop if no hashtag for 5
            # consecutive lines;
            # therefore, end of header
            if len(header_rows) and (i - header_rows[-1]) > 5:
                break

    # read .dat events file
    # with space separator regex (\s+),
    # and by skipping header rows
    events = pd.read_csv(events_file, sep="\\s+", skiprows=header_rows)

    # identify rows on which each event starts
    (event_start,) = np.where(events["#"] == 0)

    # associate each row/particle with its event
    event_col = np.empty(len(events), dtype=np.int32)
    for i, start in enumerate(event_start):
        try:
            end = event_start[i + 1]
        except IndexError:
            end = len(event_col)
        event_col[start:end] = i

    event_col = pd.Series(event_col, name="event_n", copy=False)
    events = pd.concat([event_col, events], axis=1)

    # filter for photons
    y = events[events["typ"] == 0]

    # find max number of photons per event
    n_y_max = y["#"].max()
    print(f"max {n_y_max} photons per event")

    # find number of events
    n_events = len(event_start)
    print(f"calculate inv mass for {n_events} events")

    # knowing the max number of photons per event,
    # group photons appearing in each of the events
    # into separate groups depending on their order
    # ie: every first photon of all events in group 0,
    # every second photon of all events in group 1, etc.
    # NaN if photon n does not appear in event

    y_groups = []
    indices = pd.Series(range(n_events), name="event_n")
    for i in range(1, n_y_max + 1):
        # get photon i from all events
        y_g = y[y["#"] == i].set_index("event_n")

        # create an empty dataframe filled with NaNs
        # with a row for each event, and columns for
        # the possible eta, phi and pt of a photon i
        # that would be present in event n
        group = pd.DataFrame(index=indices, columns=["eta", "phi", "pt"])

        # copy existing photon data into the
        # photon-i group
        group[["eta", "phi", "pt"]] = y_g[["eta", "phi", "pt"]]

        # accumulate the photons group
        y_groups.append(group)

    # get all combinations of picking a pair of (two)
    # photons out of a maximum of n_y_max photons:
    # effectively an n choose k problem in combinatorics
    y_combinations = combinations(range(n_y_max), 2)

    # function to get the column name of a pair of (two)
    # photons with from groups i and j
    mass_col = lambda i, j: f"M{i}{j}"

    # knowing all possible photon pairs, generate columns
    # of results dataframe
    columns = [mass_col(i, j) for i, j in y_combinations]

    # create an empty dataframe in which the resulting
    # masses of diphotons pairs will be accumulated
    mass = pd.DataFrame(index=indices, columns=columns)

    # insert a column with the number of photons in
    # each of the events
    mass.insert(0, "photons", np.bincount(y["event_n"]))

    # batch compute mass for every diphoton pair
    # the first photons of all events are in group 0,
    # the second photons of all events are
    # in group 1, etc.
    # therefore, this method generalizes to events
    # with up to n_y_max photons branching
    # (not limited to 2 or 3 photons per event

    for i, j in combinations(range(n_y_max), 2):
        # get photon group a and b, effectively
        # calculating the invariant mass for
        # diphoton pair a and b for all events
        # at once
        y_a, y_b = y_groups[i], y_groups[j]

        cosh_d_eta = np.cosh(y_a["eta"] - y_b["eta"])
        cos_d_phi = np.cos(y_a["phi"] - y_b["phi"])

        m = np.sqrt(2 * np.abs(y_a["pt"] * y_b["pt"]) * (cosh_d_eta - cos_d_phi))

        # write results of diphoton pair for
        # all events
        mass[mass_col(i, j)] = m

    # save invariant masses
    mass.to_csv(mass_file, index=True, index_label="event")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Invariant Mass Calculator")
    parser.add_argument("-i", "--input", default="TenEvents.dat")
    parser.add_argument("-o", "--output", default="TenEvents.dat_inv_mass.csv")

    args = parser.parse_args()

    main(args.input, args.output)
