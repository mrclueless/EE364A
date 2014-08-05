"""
@author: cyrusl
EE 364A Convex Optimization Midterm P1 Compressed Sensing
Due 7/26/2014
"""
import cvxpy as cvx
import numpy as np
np.random.seed(1)
(m, n) = (70, 500)
k = 10
z_true = np.zeros(n, dtype=complex)
z_true[0:k] = np.random.randn(k) + 1j * np.random.randn(k)
np.random.shuffle(z_true); z_true = np.asmatrix(z_true).T
A = np.random.randn(m, n) + 1j * np.random.randn(m, n)
A = np.asmatrix(A)
b = A*z_true; b = np.asmatrix(b)

zr = cvx.Variable(n)
zi = cvx.Variable(n)
t = cvx.Variable(m)
obj = cvx.Minimize(cvx.sum_entries(t))
#AA = cvx.norm2(cvx.hstack(cvx.vstack(A.real,A.imag),cvx.vstack(-A.imag,A.real)))
z = cvx.vstack(zr,zi)
constraints = [ cvx.norm2(cvx.hstack(cvx.vstack(A[i,:].real,A[i,:].imag),
                cvx.vstack(-A[i,:].imag,A[i,:].real))*z
                -cvx.vstack(b[i].real,b[i].imag))
                <= t[i] for i in range(m)]
'''
constraints = [ cvx.norm2(cvx.hstack(cvx.vstack(A.real,A.imag),cvx.vstack(-A.imag,A.real))*z
             - cvx.vstack(b.real,b.imag)) <= t]
'''
prob = cvx.Problem(obj, constraints)
sol = prob.solve(solver=cvx.ECOS)
print 'status: {}'.format(prob.status)
print 'norm z: {}'.format(cvx.norm2(z).value)
print 'norm z_true: {}'.format((cvx.norm2(z_true.real)+cvx.norm2(z_true.imag)).value)
for i in range(n):
    print '{} + {}j' .format(zr[i].value,zi[i].value)