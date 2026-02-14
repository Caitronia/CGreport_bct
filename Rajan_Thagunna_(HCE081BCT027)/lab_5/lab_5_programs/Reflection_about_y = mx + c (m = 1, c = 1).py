import numpy as np
import matplotlib.pyplot as plt

triangle = np.array([
    [1, 1, 1],
    [4, 1, 1],
    [2, 4, 1]
])

m = 1
c = 1
theta = np.arctan(m)

T1 = np.array([[1,0,0],[0,1,-c],[0,0,1]])
R1 = np.array([[np.cos(-theta),-np.sin(-theta),0],
               [np.sin(-theta), np.cos(-theta),0],
               [0,0,1]])

Rx = np.array([[1,0,0],[0,-1,0],[0,0,1]])

R2 = np.array([[np.cos(theta),-np.sin(theta),0],
               [np.sin(theta), np.cos(theta),0],
               [0,0,1]])

T2 = np.array([[1,0,0],[0,1,c],[0,0,1]])

final_matrix = T2 @ R2 @ Rx @ R1 @ T1

reflected = (final_matrix @ triangle.T).T

t1 = np.vstack((triangle[:, :2], triangle[0, :2]))
t2 = np.vstack((reflected[:, :2], reflected[0, :2]))

plt.plot(t1[:,0], t1[:,1], 'b-', label="Original")
plt.plot(t2[:,0], t2[:,1], 'r--', label="Reflected")
plt.gca().set_aspect('equal')
plt.grid()
plt.legend()
plt.title("Reflection about y = mx + c")
plt.show()
