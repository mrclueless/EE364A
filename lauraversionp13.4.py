# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 13:45:05 2014

@author: cyrusl
"""

import cvxpy as cvx

S = cvx.semidefinite(4)
x = cvx.vstack(0.1, 0.2, -0.05, 0.1)
obj = cvx.Maximize(x.T*S*x)

constraints =  [S[0,0] == 0.2]
constraints += [S[1,1] == 0.1]
constraints += [ S[2,2] == 0.3]
constraints += [ S[3,3] == 0.1 ]

constraints += [ S[0,1] >= 0 ]
constraints += [ S[0,2] >= 0 ] 
constraints += [ S[1,2] <= 0 ]
constraints += [ S[1,3] <= 0 ]
constraints += [ S[2,3] >= 0 ]
#constraints += [ S[0,3] == 0 ]      
prob = cvx.Problem(obj, constraints)
prob.solve()

print "status:", prob.status
print "optimal value:", sqrt(prob.value)
print "optimal covariance matrix:", S.value
