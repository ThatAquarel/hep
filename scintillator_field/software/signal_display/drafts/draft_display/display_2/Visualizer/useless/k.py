import numpy as np

raw_data = 0b011011010110101011010110

f_sc_idx = [
        [(21,20),(16,17),(13,12),(8,9),(0,1),(5,4),],
        [(22,23),(18,19),(15,14),(11,10),(2,3),(6,7),],
        ]

k = np.array([(raw_data & (2**i)) >> i for i in range(24)])[f_sc_idx]

cooked_data = [[(int(k[0]), int(k[1])) for k in k[0]], [(int(k[0]), int(k[1])) for k in k[1]]]

print(cooked_data)