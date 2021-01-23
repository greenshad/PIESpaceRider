import itertools
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
from scipy.spatial.transform import Rotation as R

arraya = np.array(list(itertools.product(*zip([1,1,1],[-1,-1,-1]))))



arraya = arraya
print(arraya)

#points = np.array([[-1, -1, -1],
                      # [1, -1, -1 ],
                      # [1, 1, -1],
                      # [-1, 1, -1],
                      # [-1, -1, 1],
                      # [1, -1, 1 ],
                      # [1, 1, 1],
                      # [-1, 1, 1]])

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# r = [-1,1]
# X, Y = np.meshgrid(r, r)
# one = np.ones(4).reshape(2, 2)
# #ax.plot_wireframe(X,Y,one, alpha=0.5)
# #ax.plot_wireframe(X,Y,-one, alpha=0.5)
# #ax.plot_wireframe(X,-one,Y, alpha=0.5)
# #ax.plot_wireframe(X,one,Y, alpha=0.5)
# #ax.plot_wireframe(one,X,Y, alpha=0.5)
# #ax.plot_wireframe(-one,X,Y, alpha=0.5)
# ax.scatter3D(points[:, 0], points[:, 1], points[:, 2])
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()

ro = R.from_euler('zyx', [0, 0, 10], degrees=True)
ri = ro.as_matrix()
print(ri)
arraye = ro.apply(arraya)

# draw cube
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("auto")
r = [-1, 1]
for s, e in combinations(arraye, 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s, e), color="b")

plt.show()

