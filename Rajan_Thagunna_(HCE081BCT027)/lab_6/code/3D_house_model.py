import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

cube = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])

roof = np.array([
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1],
    [0.5, 0.5, 1.7]   
])

cube_edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

roof_edges = [
    (0,1), (1,2), (2,3), (3,0),
    (0,4), (1,4), (2,4), (3,4)
]

def scale(points, sx, sy, sz):
    S = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, sz]
    ])
    return points @ S.T

def rotate_z(points, angle_deg):
    theta = np.radians(angle_deg)
    Rz = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])
    return points @ Rz.T

def translate(points, tx, ty, tz):
    return points + np.array([tx, ty, tz])

cube_t = scale(cube, 1.5, 1.5, 1.5)
roof_t = scale(roof, 1.5, 1.5, 1.5)

cube_t = rotate_z(cube_t, 45)
roof_t = rotate_z(roof_t, 45)

cube_t = translate(cube_t, 2, 1, 0)
roof_t = translate(roof_t, 2, 1, 0)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


for edge in cube_edges:
    pts = cube[list(edge)]
    ax.plot(pts[:,0], pts[:,1], pts[:,2], color='black')

for edge in roof_edges:
    pts = roof[list(edge)]
    ax.plot(pts[:,0], pts[:,1], pts[:,2], color='black')

for edge in cube_edges:
    pts = cube_t[list(edge)]
    ax.plot(pts[:,0], pts[:,1], pts[:,2], color='purple')

for edge in roof_edges:
    pts = roof_t[list(edge)]
    ax.plot(pts[:,0], pts[:,1], pts[:,2], color='purple')

ax.set_box_aspect([1,1,1])
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()