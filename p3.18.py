# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 16:31:36 2014

@author: cyrusl
EE 364A Convex Optimization Homework 3 A3.18 (Python Version)
Due 7/14/2014

"""
import numpy as np
import cvxpy as cvx
#from pylab import *
import matplotlib.pyplot as plt

np.random.seed(0)
n = 100
m = 300
A = np.random.rand(m,n); A = np.asmatrix(A)
b = A.dot(np.ones((n,1)))/2; b = np.asmatrix(b)
c = -np.random.rand(n,1); c= np.asmatrix(c)

x = cvx.Variable(n)
obj = cvx.Minimize(c.T*x)
constraints = [A*x <= b, x >= 0, x <= 1]          
prob = cvx.Problem(obj, constraints)

prob.solve(solver=cvx.SCS)


#print "status:", prob.status
#print "optimal value:", prob.value
#print "corresponding x:", x.value

xlrx = x
xhat = (xlrx.value).copy() # = np.zeros((n,1))

# Create threshold t and round
t = np.linspace(0,1,n)
maxviolation = np.zeros((n,1))
objective2 = np.zeros((n,1))
for i in range(0,n-1):
    for j in range(0,n-1):
        if xlrx.value[j] >= t[i]:
            xhat[j] = 1.0
        else:
            xhat[j] = 0.0
    maxviolation[i] = np.max(np.dot(A,xhat)-b)
    objective2[i] = np.dot(c.T,xhat)
    # print i, np.linalg.norm(xhat), maxviolation[i], objective2[i]

# Find least upper bound
# Find indices for which xhat is feasible
feasible = find(maxviolation <= 0)
ind = min(feasible)
U = objective2[ind]
L = np.dot(c.T,xlrx.value)
delta = U-L
print "Minimum objective value (upper bound):", U[0]
print "Lower bound:", L
print "Gap:", delta
print "Threshold t:", ind

# Find threshold values that are feasible
# for index in feasible:
#    U[i] = objective2[index]
#    t[i] = objective2[index]
#    index = index + 1


plt.figure(1)
plt.plot(t,maxviolation,t,objective2)
plt.xlabel('t')
plt.ylabel('Values')
plt.title('Max violation/Objective vs. threshold')
plt.show()
plt.legend(('Max Violation','Objective'))