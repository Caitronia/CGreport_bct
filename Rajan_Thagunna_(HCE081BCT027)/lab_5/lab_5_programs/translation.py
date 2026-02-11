import numpy as np
import matplotlib.pyplot as plt

triangle = np.array([
    [0, 0, 1],
    [2, 0, 1],
    [1, 2, 1]
])

tx = 3
ty = 2

T = np.array([
    [1, 0, tx],
    [0, 1, ty],
    [0, 0, 1]
])

translated_triangle = (T @ triangle.T).T

orig_xy = triangle[:, :2]
trans_xy = translated_triangle[:, :2]

orig_plot = np.vstack((orig_xy, orig_xy[0]))
trans_plot = np.vstack((trans_xy, trans_xy[0]))

plt.plot(orig_plot[:,0], orig_plot[:,1], 'b-')
plt.plot(trans_plot[:,0], trans_plot[:,1], 'r--')

plt.scatter(orig_xy[:,0], orig_xy[:,1], color='blue')
plt.scatter(trans_xy[:,0], trans_xy[:,1], color='red')

plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.gca().set_aspect('equal')
plt.grid(True)

plt.show()
