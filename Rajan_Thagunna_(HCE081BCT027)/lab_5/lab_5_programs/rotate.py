import numpy as np
import matplotlib.pyplot as plt

triangle = np.array([
    [1, 1, 1],
    [4, 1, 1],
    [2, 4, 1]
])

theta = np.radians(45)

R = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
    [0, 0, 1]
])

rotated_triangle = (R @ triangle.T).T

t1 = np.vstack((triangle[:, :2], triangle[0, :2]))
t2 = np.vstack((rotated_triangle[:, :2], rotated_triangle[0, :2]))

plt.plot(t1[:,0], t1[:,1], 'b-', label="Original Triangle")
plt.plot(t2[:,0], t2[:,1], 'r--', label="Rotated Triangle")

plt.scatter(triangle[:,0], triangle[:,1], color='blue')
plt.scatter(rotated_triangle[:,0], rotated_triangle[:,1], color='red')

plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.gca().set_aspect('equal')
plt.grid()
plt.legend()

plt.title("Rotation of Triangle About Origin (Homogeneous Coordinates)")
plt.show()
