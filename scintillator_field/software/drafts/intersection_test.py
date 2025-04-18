import itertools

import numpy as np

# s = np.array(
#     [
#         [
#             [0.0, 0.0],
#             [1.0, 0.0],
#         ],
#         [
#             [0.0, 1.0],
#             [1.0, 1.0],
#         ],
#     ]
# )

s = np.array(
    [
        [
            [0.0, 0.0],
            [1.0, 0.0],
        ],
        [
            [0.0, 1.0],
            [2.0, 1.0],
        ],
        [
            [0.0, 2.0],
            [4.0, 2.0],
        ],
    ]
)

v = s.reshape((-1, 2))

equations = []

for i, j in itertools.combinations(range(len(v)), 2):
    v_i = v[i]
    v_j = v[j]

    eqn = np.cross([*v_i, 1], [*v_j, 1])

    equations.append(eqn)

...

import matplotlib.pyplot as plt


def plot_lines(line_eqs, xlim=(-10, 10), ylim=(-10, 10)):
    """
    line_eqs: n x 3 array, each row [a, b, c] for line ax + by + c = 0
    xlim, ylim: limits for the plot axes
    """
    x_vals = np.linspace(xlim[0], xlim[1], 500)

    plt.figure(figsize=(8, 8))
    for a, b, c in line_eqs:
        if np.abs(b) > 1e-8:
            y_vals = (-a * x_vals - c) / b
            plt.plot(x_vals, y_vals, label=f"{a:.2f}x + {b:.2f}y + {c:.2f} = 0")
        elif np.abs(a) > 1e-8:
            x_const = -c / a
            plt.axvline(x_const, label=f"x = {x_const:.2f}")
        else:
            # Invalid line (a = b = 0)
            continue

    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.axhline(0, color="gray", linewidth=0.5)
    plt.axvline(0, color="gray", linewidth=0.5)
    plt.gca().set_aspect("equal")
    # plt.legend()
    plt.grid(True)
    plt.title("Lines from ax + by + c = 0")
    plt.show()


plot_lines(equations)
