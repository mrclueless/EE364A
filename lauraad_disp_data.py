# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 14:32:35 2014

@author: cyrusl
"""

import cvxpy as cvx
import numpy as np

np.random.seed(0)
n = 100   #number of ads
m = 30    #number of contracts
T = 60    #number of periods

#number of impressions in each period
I = 10*np.random.rand(T,1); I = np.asmatrix(I)
#revenue rate for each period and ad
R = np.random.rand(n,T); R = np.asmatrix(R)
#contract target number of impressions
q = T/float(n)*50*np.random.rand(m,1); q = np.asmatrix(q)
#penalty rate for shortfall
p = np.random.rand(m,1); p = np.asmatrix(p)
#one column per contract. 1's at the periods to be displayed
Tcontr = np.matrix(np.random.rand(T,m)>.8, dtype = float)
Acontr = np.zeros((n,m)); Acont = np.asmatrix(Acontr)
for i in range(n):
    contract=int(np.floor(m*np.random.rand(1)))
    #one column per contract. 1's at the ads to be displayed
    Acontr[i,contract]=1

#defining the variables
N = cvx.Variable(n,T)
#s = cvx.Variable(m,1)

#calculating net profit
Total_revenue = 0

for t in range(T):
    for i in range(n):
        Total_revenue = Total_revenue + R[i,t]*N[i,t]

#Penalty_payment = (p.T)*s
Penalty_payment = 0

Net_profit = Total_revenue - Penalty_payment

#defining the objective for the optimization
obj = cvx.Maximize(Net_profit)

#defining the constraints for the optimization
#constraints = [s >= 0]


constraints = [N >=0]

'''
constraints = [N[0,0] >= 0]

for i in range(n):
    for t in range(T):
        constraints += [N[i,t] >= 0]
'''
one = np.ones(T)
I_test = N*one

for t in range(T):
    constraints += [I_test[t] == I[t]]

#s_test = np.zeros(m)

#for j in range(m):
  #  Impressions_contract = 0
  #  contract_number_T = Tcontr[:,j]
  #  contract_number_A = Acontr[:,j]
   # t_contract = np.where(contract_number_T == 1)
   # i_contract = np.where(contract_number_A == 1)
   # for t in range(t_contract[0].size):
    #    for i in range(i_contract[0].size):
    #        Impressions_contract = Impressions_contract + N[i,t]
    #s_test[j] = q[j] - Impressions_contract



#Impression_contract = cvx.diag(Acontr.T*N*Tcontr)

#for j in range(m):
  #  s_test[j] = q[j] - Impression_contract[j]

#constraints += [s >= s_test]

#defining the optimization problem and solving it
prob = cvx.Problem(obj, constraints)
prob.solve(solver=cvx.SCS)

print prob.status
print Net_profit.value
#print Total_revenue.value
#print Penalty_payment.value