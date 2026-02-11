import numpy as np
import matplotlib.pyplot as plt

rect = np.array([
    [0, 0, 1],
    [4, 0, 1],
    [4, 2, 1],
    [0, 2, 1]
])

sx = 2
sy = 1.5

S = np.array([
    [sx, 0, 0],
    [0, sy, 0],
    [0, 0, 1]
])

scaled_rect = (S @ rect.T).T

r1 = np.vstack((rect[:, :2], rect[0, :2]))
r2 = np.vstack((scaled_rect[:, :2], scaled_rect[0, :2]))

plt.plot(r1[:,0], r1[:,1], 'b-', label="Original Rectangle")
plt.plot(r2[:,0], r2[:,1], 'r--', label="Scaled Rectangle")

plt.scatter(rect[:,0], rect[:,1], color='blue')
plt.scatter(scaled_rect[:,0], scaled_rect[:,1], color='red')

plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.gca().set_aspect('equal')
plt.grid()
plt.legend()

plt.title("Scaling of Rectangle About Origin (Homogeneous Coordinates)")
plt.show()

