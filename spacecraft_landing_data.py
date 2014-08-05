"""
@author: cyrusl
EE 364A Convex Optimization Homework 4 14.8 (Python Version)
Due 7/21/2014
"""

import cvxpy as cvx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

h = 1.
g = 0.1
m = 10.
Fmax = 10.
p0 = np.matrix('50;50;100')
v0 = np.matrix('-10;0;-10')
alpha = 0.5
gamma = 1.
K = 35

p = cvx.Variable(3,K+1)
v = cvx.Variable(3,K+1)
f = cvx.Variable(3,K)
e3 = np.array([[0,0,1]])
rep_e3 = np.repeat(e3,K,0)
repeat_e3 = np.asmatrix(rep_e3.T)
obj = cvx.Minimize(cvx.sum_entries(cvx.norm2(f)))

constraints = [v[:,1:K+1] == v[:,0:K] + (1/m)*f-g*repeat_e3,
               p[:,1:K+1] == p[:,0:K] + (1/2)*(v[:,0:K]+v[:,1:K+1]),
               p[:,0] == p0,
               v[:,0] == v0,
               p[:,K] == 0,
               v[:,K] == 0,
               p[2,:] >= alpha*cvx.norm2(p[0:1,:]),
               cvx.norm2(f) <= Fmax]

p = cvx.Problem(obj,constraints)
sol = p.solve(solver=cvx.SCS);

minfuel = sol*gamma*h
p_minfuel = p
v_minfuel = v
f_minfuel = f

# use the following code to plot your trajectories
# and the glide cone (don't modify)
# -------------------------------------------------------
fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.linspace(-40, 55, num=30)
Y = np.linspace(0, 55, num=30)
X, Y = np.meshgrid(X, Y)
Z = alpha*np.sqrt(X**2+Y**2)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
#Have your solution be stored in p
#ax.plot(xs=p.value[0,:].A1,ys=p.value[1,:].A1,zs=p.value[2,:].A1)
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
plt.show()
