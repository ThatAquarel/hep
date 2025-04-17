import glob
from io import StringIO
from datetime import timedelta

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from scipy.interpolate import PchipInterpolator as interp

UNIX_TIME, DATE_TIME, N = "unix_time", "time", "n"


def parse_data(data_dir):
    log_files = glob.glob(data_dir)

    trigger_data = []

    for log_file in log_files:
        with open(log_file, "r") as handle:
            lines = np.array(handle.readlines())
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


def avg_analysis(df):
    s, e = df[DATE_TIME].min(), df[DATE_TIME].max()

    print(f"FIRST: {s}")
    print(f"LAST : {e}")
    print(f"PERIOD: {e-s}")
    print()

    n, d = len(df), (e - s).total_seconds()
    print(f"N-HITS: {len(df)}")
    print(
        f"HIT-AVG: {n/d:.4f} hits/s, {n/d * 60:.4f} hits/min, {n/d * 3600:.4f} hits/hr"
    )


def sensor_p_analysis(df):
    n = df[N].to_numpy().astype(np.uint32)

    res = np.empty([len(n), 3], dtype=np.uint8)
    for i in range(3):
        byte = (n >> (8 * i)) & 0xFF
        res[:, 2 - i] = byte
    bits = np.unpackbits(res, axis=1)

    sensor_on_time = np.mean(bits, axis=0)
    on_time_str = "".join(
        [
            f"{t * 100:4.1f}%{' | ' if (i % 8 == 7) else ' '}"
            for i, t in enumerate(sensor_on_time)
        ]
    )
    print(on_time_str)

    complementary_sums = sensor_on_time.reshape((-1, 2)).sum(axis=1)
    c_on_time_str = "".join(
        [
            f"{t * 100:5.1f}%     {'  | ' if (i % 4 == 3) else ' '}"
            for i, t in enumerate(complementary_sums)
        ]
    )
    print(c_on_time_str)


def fit(x, y, window=16):
    moving_avg = np.convolve(y, np.ones(window), "valid") / window
    return x[: len(moving_avg)], moving_avg


def graph_alt(df):
    # === Time delta plots ===
    timestamps = df[DATE_TIME]
    t = df[UNIX_TIME].to_numpy()

    dt = t[1:] - t[:-1]
    x = timestamps[:-1]

    min_x, max_x = x.min(), x.max()

    # Start at first midnight
    current = min_x.replace(hour=0, minute=0, second=0, microsecond=0)
    if current < min_x:
        current += timedelta(days=1)

    # === Create Figure and Subplots ===
    fig, axs = plt.subplots(6, 1, figsize=(12, 18), sharex=False)

    # Plot 1: Seconds per hit
    axs[0].plot(x, dt, label="Raw")
    axs[0].plot(*fit(x, dt), label="Moving Avg")
    axs[0].set_yscale("log")
    axs[0].set(xlabel="Time", ylabel="s/hit", title="Seconds per hit")
    axs[0].grid(True)
    axs[0].legend()

    # Plot 2: Hits per second
    hits_per_sec = 1 / dt
    axs[1].plot(x, hits_per_sec, label="Raw")
    axs[1].plot(*fit(x, hits_per_sec), label="Moving Avg")
    axs[1].set_yscale("log")
    axs[1].set(xlabel="Time", ylabel="hit/s", title="Hits per second")
    axs[1].grid(True)
    axs[1].legend()

    # Midnights
    midnight = current
    while midnight <= max_x:
        for i in range(3):
            axs[i].axvline(midnight, color="blue", linestyle='--', linewidth=1)
            axs[i].axvline(midnight + timedelta(hours=12), color="red", linestyle='--', linewidth=1)
        midnight += timedelta(days=1)

    # Plot 3: Hits per second (non-log scale)
    axs[2].plot(x, hits_per_sec, label="Raw")
    axs[2].plot(*fit(x, hits_per_sec), label="Moving Avg")
    axs[2].set(xlabel="Time", ylabel="hit/s", title="Hits per second (linear)")
    axs[2].grid(True)
    axs[2].legend()

    # Format date on x-axis
    for ax in axs[:3]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    # === FFT Analysis ===

    # Prepare interpolation
    sample_per_second = 10
    x_non_uniform = t[:-1]
    x_dt = x_non_uniform.max() - x_non_uniform.min()
    x_uniform = np.linspace(x_non_uniform.min(), x_non_uniform.max(), int(x_dt * sample_per_second))

    y_signal = np.log(hits_per_sec)
    interpolator = interp(x_non_uniform, y_signal)
    y_uniform = interpolator(x_uniform)

    # FFT
    fft_result = np.fft.fft(y_uniform)
    freq = np.fft.fftfreq(len(x_uniform), 1 / sample_per_second)

    # Plot 4: Interpolation
    axs[3].plot(x_non_uniform, y_signal, "bo", label="Non-uniform")
    axs[3].plot(x_uniform, y_uniform, "r-", label="Interpolated")
    axs[3].legend()
    axs[3].set(title="Interpolated Signal", ylabel="log(hit/s)")

    # Plot 5: Full FFT
    axs[4].plot(freq[:len(freq)//2], np.abs(fft_result)[:len(freq)//2])
    axs[4].set(title="FFT (Full Spectrum)", xlabel="Frequency (Hz)", ylabel="Amplitude")

    # Plot 6: Zoomed FFT
    scale = 1 << 16
    axs[5].plot(freq[:len(freq)//scale], np.abs(fft_result)[:len(freq)//scale])
    axs[5].axvline(1 / (3600 * 24), color="red", label="24h")
    axs[5].axvline(1 / (3600 * 12), color="green", label="12h")
    axs[5].axvline(1 / (3600 * 24 * 7), color="black", label="7d")
    axs[5].set(title="FFT (Zoomed)", xlabel="Frequency (Hz)", ylabel="Amplitude")
    axs[5].legend()

    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()


def main():
    df = parse_data("scintillator_field/data/sc_data*")

    avg_analysis(df)
    sensor_p_analysis(df)

    graph_alt(df)
    ...


if __name__ == "__main__":
    main()
