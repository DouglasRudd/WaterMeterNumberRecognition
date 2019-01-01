import numpy as np
import csv


x = np.linspace(0.0, 6.0, 100)
y = np.cos(x)

writer = csv.writer(open("some.csv", "w"))
writer.writerows(zip(x, y))