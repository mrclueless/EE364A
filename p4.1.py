# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 09:40:59 2014

@author: cyrusl
EE 364A Convex Optimization Homework 2 4.1
Due 7/7/2014
"""
from cvxpy import *

# Create two scalar optimization variables.
x = Variable()
y = Variable()

# Create two constraints.
constraints = [2*x + y >= 1,
               x + 3*y >= 1,
               x >= 0, y >= 0]

# Form objective.
obj1 = Minimize(x + y)
obj2 = Minimize(-x - y)
obj3 = Minimize(x)
obj4 = Minimize(max_elemwise(x,y))
obj5 = Minimize(square(x) + 9 * square(y))

# Form and solve problem. (a)
prob1 = Problem(obj1, constraints)
prob1.solve()  # Returns the optimal value.
print "(a) status:", prob1.status
print "(a) optimal value", prob1.value
print "(a) optimal var", x.value, y.value

# Form and solve problem.(b)
prob2 = Problem(obj2, constraints)
prob2.solve()  # Returns the optimal value.
print "(b) status:", prob2.status
print "(b) optimal value", prob2.value
print "(b) optimal var", x.value, y.value

# Form and solve problem (c)
prob3 = Problem(obj3, constraints)
prob3.solve()  # Returns the optimal value.
print "(c) status:", prob3.status
print "(c) optimal value", prob3.value
print "(c) optimal var", x.value, y.value

# Form and solve problem (d)
prob4 = Problem(obj4, constraints)
prob4.solve()  # Returns the optimal value.
print "(d) status:", prob4.status
print "(d) optimal value", prob4.value
print "(d) optimal var", x.value, y.value

# Form and solve problem (e)
prob5 = Problem(obj5, constraints)
prob5.solve()  # Returns the optimal value.
print "(e) status:", prob5.status
print "(e) optimal value", prob5.value
print "(e) optimal var", x.value, y.value