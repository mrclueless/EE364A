# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 19:00:42 2014

@author: cyrusl
"""
import cvxpy as cvx
import numpy as np

ad_disp_data.py

'''        
N = cvx.Variable(n,T)     # display number
obj = cvx.Maximize(R.T*N-p.T*(cvx.pos(q-cvx.diag(Acontr.T*N*Tcontr))))
constraints = [N >= 0, cvx.sum(N).T == I]
prob = cvx.solve(obj, constraints)

print "status:", prob.status
print "optimal s:", prob.value
print "optimal case penalty:", prob.value
print "optimal case revenue:", prob+p.T*prob.value
'''
# Displaying without contracts
Nignore = cvx.Variable(n,T)
obj2 = cvx.Maximize(R.T*Nignore)
constraints2 = [N >= 0, cvx.sum(N).T == I]
prob2 = cvx.solve(obj2, constraints2)
s2 = cvx.pos(q-cvx.diag(Acontr.T*Nignore*Tcontr))
net_profit = prob2.value - p.T*s2
penalty =  p.T*s2
revenue = prob2.value
