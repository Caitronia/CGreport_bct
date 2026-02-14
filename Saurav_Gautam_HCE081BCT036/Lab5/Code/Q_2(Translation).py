import numpy as np
import matplotlib.pyplot as plt

vertices = np.array([
    [0, 0, 1],
    [2, 0, 1],
    [1, 2, 1]
])

dx, dy = 3, 2

transform = np.array([
    [1, 0, dx],
    [0, 1, dy],
    [0, 0, 1]
])

result = (transform @ vertices.T).T

orig = vertices[:, :2]
moved = result[:, :2]

orig_path = np.vstack([orig, orig[0]])
moved_path = np.vstack([moved, moved[0]])

plt.plot(orig_path[:, 0], orig_path[:, 1], color='blue')
plt.plot(moved_path[:, 0], moved_path[:, 1], linestyle='--', color='red')

plt.scatter(orig[:, 0], orig[:, 1])
plt.scatter(moved[:, 0], moved[:, 1])

plt.axhline(0)
plt.axvline(0)
plt.gca().set_aspect('equal')
plt.grid(True)

plt.show()