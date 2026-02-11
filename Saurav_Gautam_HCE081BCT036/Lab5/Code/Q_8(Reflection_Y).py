import numpy as np
import matplotlib.pyplot as plt

pts = np.array([[0, 0, 1], [2, 0, 1], [1, 2, 1]], dtype=float)

M = np.array([
    [-1, 0, 0],
    [0,  1, 0],
    [0,  0, 1]
], dtype=float)

out = (M @ pts.T).T

a = pts[:, :2]
b = out[:, :2]
a2 = np.vstack([a, a[0]])
b2 = np.vstack([b, b[0]])

plt.plot(a2[:, 0], a2[:, 1], color="blue")
plt.plot(b2[:, 0], b2[:, 1], linestyle="--", color="red")
plt.scatter(a[:, 0], a[:, 1])
plt.scatter(b[:, 0], b[:, 1])
plt.axhline(0); plt.axvline(0)
plt.gca().set_aspect("equal")
plt.grid(True)
plt.show()