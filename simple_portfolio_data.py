"""
@author: cyrusl
EE 364A Convex Optimization Homework 4 13.3 (Python Version)
Due 7/21/2014
"""
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt

np.random.seed(1)
n = 20
pbar = np.ones((n,1))*.03 + np.r_[np.random.rand(n-1,1), np.zeros((1,1))]*.12;
S = np.random.randn(n, n); S = np.asmatrix(S)
S = S.T*S
S = S/max(np.abs(np.diag(S)))*.2
S[:, -1] = np.zeros((n, 1))
S[-1, :] = np.zeros((n, 1)).T
x_unif = np.ones((n, 1))/n; x_unit = np.asmatrix(x_unif)

# Part (a) Find minimum-risk portfolios
print('Part (a) Find minimum-risk portfolios')
pbarm =  np.asmatrix(pbar)
r_min = pbarm.T*x_unit
risk_uniform = cvx.quad_form(x_unif, S).value
x = cvx.Variable(n)
obj_a = cvx.Minimize( cvx.quad_form(x,S) )

#No (additional) constraints
constraints_i = [pbarm.T * x == r_min, cvx.sum_entries(x)== 1]
prob_ai = cvx.Problem(obj_a, constraints_i)
risk_ai = prob_ai.solve()

#Long-only
constraints_ii = [pbarm.T * x == r_min, cvx.sum_entries(x)== 1 , x >= 0]
prob_aii = cvx.Problem(obj_a, constraints_ii)
risk_aii = prob_aii.solve()

#Limit on total short position
#one = np.matrix(np.ones((n, 1)))
constraints_iii = [pbarm.T * x == r_min, cvx.sum_entries(x)== 1]
for i in range (n):
    constraints_iii += [1 * cvx.neg(x[i]) <= 0.5]
prob_aiii = cvx.Problem(obj_a, constraints_iii)
risk_aiii = prob_aiii.solve()

print('Uniform portfolio risk: {}'.format(risk_uniform))
print('No (additional) constraints risk: {}'.format(risk_ai))
print('Long-only risk: {}'.format(risk_aii))
print('Limit on total short position risk: {}'.format(risk_aiii))

# Part (b) Plot optimal risk-return trade-off curves
mus = np.logspace(0, 5, n)
mean_long = np.zeros(n)
std_long = np.zeros(n)
mean_totalshort = np.zeros(n)
std_totalshort = np.zeros(n)
constraints_long = [cvx.sum_entries(x) == 1, x>= 0]
constraints_totalshort = [cvx.sum_entries(x )== 1]
for i in range (n):
    constraints_totalshort += [1 * cvx.neg(x[i]) <= 0.5]
for i, mu in enumerate(mus):
    #print('mu = {}', format(mu))
    objective = cvx.Minimize(-pbarm.T*x + mu * cvx.quad_form(x,S) )
    
    #Long-only
    prob_long = cvx.Problem(objective, constraints_long)
    prob_long.solve()
    #print('status ={}',prob_long.status)
    mean_long[i] = (pbarm.T*x).value                    #return
    std_long[i] = cvx.sqrt(cvx.quad_form(x,S)).value  #sqrt(risk)
    
    #Total short
    prob_totalshort = cvx.Problem(objective, constraints_totalshort)
    prob_totalshort.solve()
    #print('status ={}',prob_long.status)
    mean_totalshort[i] = (pbarm.T*x).value                    #return
    std_totalshort[i] = cvx.sqrt(cvx.quad_form(x,S)).value  #sqrt(risk)
    
plt.plot(std_long, mean_long, label='long-only')
plt.plot(std_totalshort,mean_totalshort, label='total short')
plt.xlabel('standard deviation of return')
plt.ylabel('mean return')
plt.legend(loc='lower right', frameon=False);