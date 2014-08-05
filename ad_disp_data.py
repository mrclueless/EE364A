'''
@author: cyrusl
EE 364A Convex Optimization Homework 3 A17.4 Online Advertising Display
Due 7/14/2014
'''

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
'''    
N = cvx.Variable(n,T)
obj = cvx.Maximize(cvx.sum_entries(cvx.mul_elemwise(R, N))
                    - p.T*cvx.pos(q-cvx.diag(Acontr.T*N*Tcontr)))
constraints = [N >= 0]
for j in range(T):
    constraints.append(
    cvx.sum_entries(N[:,j]) == I[j] )
prob = cvx.Problem(obj, constraints)
prob.solve(solver=cvx.SCS)

s1 = cvx.pos(q-cvx.diag(Acontr.T*N*Tcontr));
optimal_net_profit = prob.value
optimal_penalty = p.T*s1
optimal_revenue = optimal_penalty + optimal_net_profit
print "status:", prob.status
print "optimal net profit:", optimal_net_profit
print "optimal penalty:", prob.value
print "optimal revenue:", prob+p.T*prob.value
'''
# Greedy Aproach displaying without contracts
Nignore = cvx.Variable(n,T)
obj2 = cvx.Maximize(cvx.sum_entries(cvx.mul_elemwise(R, Nignore))) #np.reshape(R,n*T).T *Nignore[:,:])
constraints2 = [Nignore >= 0]
for j in range(T):
    constraints2.append(
    cvx.sum_entries(Nignore[:,j]) == I[j] )
prob2 = cvx.Problem(obj2, constraints2)
prob2.solve()

s2 = cvx.pos(q-cvx.diag(Acontr.T*Nignore*Tcontr))
greedy_net_profit = prob2.value - p.T*s2
greedy_penalty =  p.T*s2
print "greedy status:", prob2.status
print "greedy net_profit:", greedy_net_profit.value
print "greedy penalty:", greedy_penalty.value
print "greedy revenue:", prob2.value