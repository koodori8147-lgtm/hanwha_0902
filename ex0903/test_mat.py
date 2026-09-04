import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np

ypoints = np.array([2.5, 1.1, 0.5, 0.2, 0.4, 0.8, 1.5, 1.7, 3.5])

plt.plot(ypoints, marker='o')

plt.show()