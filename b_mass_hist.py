import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main(
    inv_mass_file,
    start_m=100,
    end_m=160,
    bin_width=2,
    sb_fit_ndeg=32,
    b_fit_ndeg=4,
):
    events = pd.read_csv(inv_mass_file, index_col="event")
    pair_cols = [col for col in events.columns if col.startswith("M")]

    inv_mass = events[pair_cols]
    mass = inv_mass.to_numpy().flatten()

    mass = mass[~np.isnan(mass)]
    mass = mass[(mass > start_m) & (mass < end_m)]

    n_bins = (end_m - start_m) // bin_width
    bin_edges = np.arange(n_bins) * bin_width + start_m

    hist, bin_edges = np.histogram(mass, bins=bin_edges)
    x, y = bin_edges[:-1], hist

    sb_coeffs = np.polyfit(x, y, sb_fit_ndeg)
    b_coeffs = np.polyfit(x, y, b_fit_ndeg)

    fit_sb, fit_b = np.poly1d(sb_coeffs), np.poly1d(b_coeffs)

    y_sb, y_b = fit_sb(x), fit_b(x)

    fig, (sb, s) = plt.subplots(2, 1, height_ratios=[2, 1])
    fig.subplots_adjust(hspace=0)
    sb.set_title("Higgs Decay Through Diphoton Channel")

    sb.scatter(x, y, color="black", label="$Data$")
    sb.plot(
        x, y_sb, color="red", label=f"$Sig+Bkg\\ ({sb_fit_ndeg}\\ deg\\ poly\\ fit)$"
    )
    sb.plot(
        x, y_b, ":", color="red", label=f"$Bkg\\ ({b_fit_ndeg}\\ deg\\ poly\\ fit)$"
    )
    sb.tick_params(axis="x", which="both", bottom=False, labelbottom=False)

    sb.set_ylabel(f"$Events\\ /\\ {bin_width}\\ GeV$")

    s.scatter(x, (y - y_b) / np.sqrt(y_b), color="black")
    s.plot(x, (y_sb - y_b) / np.sqrt(y_b), color="red")
    s.plot(x, (y_b - y_b) / np.sqrt(y_b), ":", color="red")

    s.set_ylabel(f"$Significance$")
    s.set_xlabel("$m_{\\gamma\\gamma} (GeV)$")
    sb.legend(loc="upper right")

    plt.show()


if __name__ == "__main__":
    plt.rcParams["text.usetex"] = True

    parser = argparse.ArgumentParser(prog="Higgs Histogram")
    parser.add_argument("-i", "--input", default="inv_mass.csv")

    args = parser.parse_args()

    main(args.input)
