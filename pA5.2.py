"""
@author: cyrusl
EE 364A Convex Optimization Homework 5 A5.2 Minimax rational fit
Due 7/25/2014
"""
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt

k = 201
t = np.asmatrix(np.linspace(-3,3,k)).T
y = np.exp(t)
one = np.asmatrix(np.ones((k,1)))
Tpow = cvx.hstack(one, t, cvx.square(t))
u = np.exp(3)
l = 0
tol = 1e-3

while u-l >= tol:
    mid = (l+u)/2
    a = cvx.Variable(3)
    b = cvx.Variable(2)
    obj = cvx.Minimize(0)
    constraints = [cvx.abs(Tpow*a - cvx.mul_elemwise(y, Tpow*cvx.vstack(1, b)))
                    <= mid * Tpow*cvx.vstack(1, b)]          
    prob = cvx.Problem(obj, constraints)
    sol = prob.solve(solver=cvx.CVXOPT)
    if prob.status == cvx.OPTIMAL:
        print('gamma = {}', format(mid))
        u = mid
        a_opt = a
        b_opt = b
        objval_opt = mid
    else:
        l = mid
        
y_fit = cvx.mul_elemwise(Tpow*a_opt.value,
                         cvx.inv_pos(Tpow*cvx.vstack(1, b_opt.value)))
plt.figure(0)
plt.plot(t.A1, y.A1, label='y')
plt.plot(t.A1, y_fit.value.A1,'g-o', label='fit')
plt.xlabel('t')
plt.ylabel('y')
plt.title('A5.2: Fit vs. Exponential Function')
plt.legend(loc='lower right', frameon=False);
plt.figure(1)
plt.plot(t.A1,y_fit.value.A1-y.A1)
plt.xlabel('t')
plt.ylabel('error')
plt.title('A5.2: Fitting Error Plot')
print('a: {}'.format(a_opt.T.value))
print('b: {}'.format(b_opt.T.value))
print('optimal objective value: {}'.format(mid))