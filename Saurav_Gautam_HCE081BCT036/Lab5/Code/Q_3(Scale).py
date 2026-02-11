import numpy as np
import matplotlib.pyplot as plt

shape = np.array([
    [0, 0, 1],
    [2, 0, 1],
    [1, 2, 1]
], dtype=float)

sx, sy = 5, 2

scale_mat = np.array([
    [sx, 0,  0],
    [0,  sy, 0],
    [0,  0,  1]
], dtype=float)

scaled = (scale_mat @ shape.T).T

p = shape[:, :2]
q = scaled[:, :2]

p_closed = np.vstack([p, p[0]])
q_closed = np.vstack([q, q[0]])

plt.plot(p_closed[:, 0], p_closed[:, 1], color='blue')
plt.plot(q_closed[:, 0], q_closed[:, 1], linestyle='--', color='red')

plt.scatter(p[:, 0], p[:, 1])
plt.scatter(q[:, 0], q[:, 1])

plt.axhline(0)
plt.axvline(0)
plt.gca().set_aspect('equal')
plt.grid(True)

plt.show()