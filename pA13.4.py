# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 15:46:56 2014

@author: cyrusl
EE 364A Convex Optimization Homework 3 A13.4
Due 7/14/2014
"""
import cvxpy as cvx

S = cvx.semidefinite(4)
x = cvx.vstack(0.1, 0.2, -0.05, 0.1)
obj = cvx.Maximize(x.T*S*x)
constraints = [S[0,0] == 0.2,
            S[1,1] == 0.1,
            S[2,2] == 0.3,
            S[3,3] == 0.1,
            S[0,1] >= 0,
            S[0,2] >= 0,
            S[1,2] <= 0,
            S[1,3] <= 0,
            S[2,3] >= 0]            
prob = cvx.Problem(obj, constraints)
prob.solve()

print "status:", prob.status
print "optimal value:", sqrt(prob.value)
print "optimal covariance matrix:", S.value

# when sigma is diagonal
constraints2 = [S[0,0] == 0.2,
            S[1,1] == 0.1,
            S[2,2] == 0.3,
            S[3,3] == 0.1,
            S[0,1] == 0,
            S[0,2] == 0,
            S[1,2] == 0,
            S[1,3] == 0,
            S[2,3] == 0,
            S[3,0] == 0]
prob2 = cvx.Problem(obj,constraints2)
prob2.solve()
print "status:", prob2.status
print "risk when sigma is diagonal:", sqrt(prob2.value)
print "the diagonal covariance matrix:", S.value