import glob
from io import StringIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


(file,) = glob.glob("scintillator_field/software/long_term/*.log")
with open(file, "r") as handle:
    lines = handle.readlines()

cleaned = []

i = 0
while i < len(lines):
    current_line = lines[i]
    i += 1

    if "INFO:RECORDER:start recorder" in current_line:
        continue

    if not current_line.startswith("INFO:RECORDER:"):
        continue

    time_n = current_line.removeprefix("INFO:RECORDER:")
    cleaned.append(time_n)


str_io = StringIO("".join(cleaned))

UNIX_TIME, TIME, N = "unix_time", "time", "n"

data = pd.read_csv(str_io, header=None, names=[UNIX_TIME, N])
# data[TIME] = pd.to_datetime(data[UNIX_TIME], unit="s", utc=True).dt.tz_convert('America/Toronto')
data[TIME] = pd.to_datetime(data[UNIX_TIME], unit="s", utc=True).dt.tz_convert(
    "America/Toronto"
)

s, e = data[TIME].min(), data[TIME].max()

print(f"FIRST: {s}")
print(f"LAST : {e}")
print(f"PERIOD: {e-s}")
print()

n, d = len(data), (e - s).total_seconds()
print(f"N-HITS: {len(data)}")
print(f"HIT-AVG: {n/d:.4f} hits/s, {n/d * 60:.4f} hits/min, {n/d * 3600:.4f} hits/hr")


n = data[N].to_numpy().astype(np.uint32)
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

...


def fit(x, y, window=16):
    moving_avg = np.convolve(y, np.ones(window), "valid") / window
    return x[: len(moving_avg)], moving_avg


# TODO: moving average of hits/second, graph

timestamps = data[TIME]

t = data[UNIX_TIME].to_numpy()
dt = t[1:] - t[:-1]
# x_t = t[:-1]
x = timestamps[:-1]

fig, (ax, ax0) = plt.subplots(2)
ax.plot(x, dt)
ax.plot(*fit(x, dt))

ax.set_yscale("log")
ax.set(xlabel="time (s)", ylabel="s/hit")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
fig.autofmt_xdate()
ax.grid(True)

ax0.plot(x, 1 / dt)
ax0.plot(*fit(x, 1 / dt))
ax.set(xlabel="time (s)", ylabel="hit/s")
ax0.set_yscale("log")

ax0.grid(True)


plt.show()
...


from scipy.interpolate import interp1d

sample_per_second = 4

x_non_uniform = t[:-1]
x_dt =  x_non_uniform.max() -  x_non_uniform.min()
x_uniform = np.linspace(x_non_uniform.min(), x_non_uniform.max(), int(x_dt * sample_per_second))
y_signal = np.log(1/dt)

interpolator = interp1d(x_non_uniform, y_signal, kind='linear', fill_value="extrapolate")
y_uniform = interpolator(x_uniform)

fft_result = np.fft.fft(y_uniform)
freq = np.fft.fftfreq(len(x_uniform), 1/sample_per_second)


plt.subplot(3, 1, 1)
plt.plot(x_non_uniform, y_signal, 'bo', label='Non-uniform data')
plt.plot(x_uniform, y_uniform, 'r-', label='Interpolated data')
plt.legend()
plt.title('Non-uniform data and interpolated signal')

plt.subplot(3, 1, 2)
plt.plot(freq[:len(freq)//2], np.abs(fft_result)[:len(freq)//2])  # Only plot positive frequencies
plt.title('FFT of Interpolated Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

plt.subplot(3, 1, 3)
plt.plot(freq[:len(freq)//4096], np.abs(fft_result)[:len(freq)//4096])  # Only plot positive frequencies
plt.title('FFT of Interpolated Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')



plt.tight_layout()
plt.show()
