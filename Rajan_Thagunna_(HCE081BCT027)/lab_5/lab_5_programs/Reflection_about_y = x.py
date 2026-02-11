import numpy as np
import matplotlib.pyplot as plt

triangle = np.array([
    [1, 1, 1],
    [4, 1, 1],
    [2, 4, 1]
])

Ryx = np.array([
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, 1]
])

reflected = (Ryx @ triangle.T).T

t1 = np.vstack((triangle[:, :2], triangle[0, :2]))
t2 = np.vstack((reflected[:, :2], reflected[0, :2]))

plt.plot(t1[:,0], t1[:,1], 'b-', label="Original")
plt.plot(t2[:,0], t2[:,1], 'r--', label="Reflected")
plt.gca().set_aspect('equal')
plt.grid()
plt.legend()
plt.title("Reflection about y = x")
plt.show()
