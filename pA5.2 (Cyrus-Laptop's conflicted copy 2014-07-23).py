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

#print('status: {}'.format(sol))
#print('theta: {}'.format(theta.value))
#print('t: {}'.format(t))
#print('y: {}'.format(y))

while u-1 >= tol:
    gamma = (l+u)/2
    a = cvx.Variable(3)
    b = cvx.Variable(2)
    obj = cvx.Minimize(0)
    constraints = [cvx.abs(Tpow*a - cvx.mul_elemwise(y, Tpow*cvx.vstack(1, b)))<= gamma * Tpow*cvx.vstack(1, b)]          
    prob = cvx.Problem(obj, constraints)
    sol = prob.solve(solver=cvx.SCS)
    if prob.status == cvx.OPTIMAL:
        print('gamma = {}'.format(gamma))
        u = gamma
        a_opt = a
        b_opt = b
        objval_opt = gamma
    else:
        l = gamma

left = Tpow*a_opt.value
right = Tpow*cvx.vstack(1, b_opt.value)
y_fit = np.asmatrix(np.zeros((k,1)))
for i in range(left.size[0]):
    y_fit[i] = left[i].value/right[i].value

plt.figure(0)
plt.plot(t.A1, y.A1, label='y')
plt.plot(t.A1, (y_fit).A1, label='fit')
plt.xlabel('t')
plt.ylabel('y')

plt.figure(1)
plt.plot(t.A1,(y_fit).A1-y.A1)
plt.xlabel('t')
plt.ylabel('error')

print('a_opt = {}'.format(a_opt.value))
print('b_opt = {}'.format(b_opt.value))