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

#Solution begins
#--------------------------------------------------------------
e3 = np.matrix('0;0;1')
p = cvx.Variable(3,K+1)
v = cvx.Variable(3,K+1)
f = cvx.Variable (3,K)
fuel_use = h*gamma*sum([cvx.norm(f[:,i]) for i in range(K)])
const = [v[:,i+1] == v[:,i] + (h/m)*f[:,i]-h*g*e3 for i in range(K)]
const += [p[:,i+1] == p[:,i] + h/2*(v[:,i]+v[:,i+1]) for i in range(K)]
const += [p[:,0]==p0, v[:,0]==v0]
const += [p[:,K]==0, v[:,K]==0]
const += [p[2,i] >= alpha*cvx.norm(p[0:2,i]) for i in range(K+1)]
const += [cvx.norm(f[:,i]) <= Fmax for i in range(K)]
prob = cvx.Problem(cvx.Minimize(fuel_use), const)
prob.solve()
print 'Minimum fuel use is %.2f' % fuel_use.value
# Minimum fuel trajectory and glide cone
fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.linspace(-40, 55, num=30)
Y = np.linspace(0, 55, num=30)
X, Y = np.meshgrid(X, Y)
Z = alpha*np.sqrt(X**2+Y**2);
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
ax.plot(xs=p.value[0,:].A1,ys=p.value[1,:].A1,zs=p.value[2,:].A1)
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')

#For minimum time descent, we do a linear search but bisection would be faster.
K = 1
while True:
    p = cvx.Variable(3,K+1)
    v = cvx.Variable(3,K+1)
    f = cvx.Variable (3,K)
    const = [v[:,i+1] == v[:,i] + (h/m)*f[:,i]-h*g*e3 for i in range(K)]
    const += [p[:,i+1] == p[:,i] + h/2*(v[:,i]+v[:,i+1]) for i in range(K)]
    const += [p[:,0]==p0, v[:,0]==v0]
    const += [p[:,K]==0, v[:,K]==0]
    const += [p[2,i] >= alpha*cvx.norm(p[0:2,i]) for i in range(K+1)]
    const += [cvx.norm(f[:,i]) <= Fmax for i in range(K)]
    prob = cvx.Problem(cvx.Minimize(0), const)
    prob.solve()
    if prob.status=='optimal':
        break
    K += 1
print 'The minimum touchdown time is', K
#Minimum time trajectory and glide cone
fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.linspace(-40, 55, num=30)
Y = np.linspace(0, 55, num=30)
X, Y = np.meshgrid(X, Y)
Z = alpha*np.sqrt(X**2+Y**2);
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
ax.plot(xs=p.value[0,:].A1,ys=p.value[1,:].A1,zs=p.value[2,:].A1)
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
plt.show()
