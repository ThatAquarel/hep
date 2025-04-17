import numpy as np


a = np.array([0, 1, 2, 3, 4, 5, 6, 7])
idx = [
    [0, 7],
    [1, 6],
    [2, 5],
    [3, 4],
]
b = a[idx]

print(a)
print(b)

c = np.array([p[0]*p[1] for p in b])
print(c)