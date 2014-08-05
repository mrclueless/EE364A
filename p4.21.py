# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 11:33:31 2014

@author: cyrusl
EE 364A Convex Optimization Homework 4 4.21 (Python Version)
Due 7/21/2014
"""
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt

np.random.seed(10)
(m, n) = (30, 10)
A = np.random.rand(m,n); A = np.asmatrix(A)
b = np.random.rand(m,1); b = np.asmatrix(b)
c_nom = np.ones((n,1)) + np.random.rand(n,1); c_nom = np.asmatrix(c_nom)

F = cvx.vstack(np.matrix(np.identity(n)), -np.matrix(np.identity(n)),
     1/n*np.matrix(np.ones((1,n))), -1/n* np.matrix(np.ones((1,n))))
g = cvx.vstack(1.25 *c_nom, -0.75*c_nom, 1.1/n*cvx.sum_entries(c_nom),
               -0.9/n*cvx.sum_entries(c_nom))

# robust LP
x = cvx.Variable(n)
lambd = cvx.Variable(g.size[0])
obj = cvx.Minimize(lambd.T*g)
constraints = [A*x >= b, lambd >= 0, F.T *lambd == x]          
prob = cvx.Problem(obj, constraints)

#prob.solve(solver=cvx.SCS)
prob.solve()
print "status:", prob.status
print "nominal cost (robust case):", (c_nom.T * x).value
print "f(x):", prob.value

# nominal LP
x_nom = cvx.Variable(n)
obj2 = cvx.Minimize(c_nom.T*x_nom)
constraints2 = [A*x_nom >= b]
prob2 = cvx.Problem(obj2, constraints2)

prob2.solve()
print "status:", prob2.status
print "nominal cost (nominal case):", (c_nom.T * x_nom).value

x_nomin =(x_nom.value).copy()

# worst case cost of x_nom
c_worst = cvx.Variable(n)
obj3 = cvx.Maximize(c_worst.T*x_nomin)
constraints3 = [F*c_worst <= g]
prob3 = cvx.Problem(obj3, constraints3)
prob3.solve()
print "status:", prob3.status
print "f(x):", prob3.value