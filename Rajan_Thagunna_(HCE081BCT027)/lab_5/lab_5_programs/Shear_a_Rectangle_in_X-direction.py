import numpy as np
import matplotlib.pyplot as plt

rectangle = np.array([
    [0, 0, 1],
    [4, 0, 1],
    [4, 2, 1],
    [0, 2, 1]
])

shx = 1

Shx = np.array([
    [1, shx, 0],
    [0, 1, 0],
    [0, 0, 1]
])

sheared = (Shx @ rectangle.T).T

r1 = np.vstack((rectangle[:, :2], rectangle[0, :2]))
r2 = np.vstack((sheared[:, :2], sheared[0, :2]))

plt.plot(r1[:,0], r1[:,1], 'b-', label="Original Rectangle")
plt.plot(r2[:,0], r2[:,1], 'r--', label="Sheared (X-direction)")

plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.gca().set_aspect('equal')
plt.grid()
plt.legend()
plt.title("Shearing in X-direction")
plt.show()
