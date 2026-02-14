import numpy as np
import matplotlib.pyplot as plt
import math

pts = np.array([
    [0, 0, 1],
    [2, 0, 1],
    [1, 2, 1]
], dtype=float)

angle_deg = 45
theta = math.radians(angle_deg)

rot = np.array([
    [math.cos(theta), -math.sin(theta), 0],
    [math.sin(theta),  math.cos(theta), 0],
    [0,               0,               1]
], dtype=float)

rotated = (rot @ pts.T).T

a = pts[:, :2]
b = rotated[:, :2]

a_closed = np.vstack([a, a[0]])
b_closed = np.vstack([b, b[0]])

plt.plot(a_closed[:, 0], a_closed[:, 1], color='blue')
plt.plot(b_closed[:, 0], b_closed[:, 1], linestyle='--', color='red')

plt.scatter(a[:, 0], a[:, 1])
plt.scatter(b[:, 0], b[:, 1])

plt.axhline(0)
plt.axvline(0)
plt.gca().set_aspect('equal')
plt.grid(True)

plt.show()