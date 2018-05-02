#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from densities.banana import Banana
from samplers.mcmc.hmc import StaticHMC

np.random.seed(1234)

bananicity = 0.1
target = Banana(bananicity)

ndim = 2
nsamples = 100
#start = np.array([0., 10.])
start = np.array([-20., -30.])

stepsize = .3
nsteps = 50
sampler = StaticHMC(ndim, target.pdf, target.log_pdf_gradient, stepsize, stepsize, nsteps, nsteps)

samples = sampler.sample(nsamples, start)

n_accepted = 1
for i in range(1, nsamples):
    if (samples[i] != samples[i-1]).any():
            n_accepted += 1

print('Acceptance rate:', n_accepted/nsamples)


a = np.sqrt(599)
b = np.sqrt(5.99)
x = np.linspace(-a, a, 200)
ellipse = b/a*np.sqrt(a**2-x**2)
contour1 = ellipse - bananicity*x**2 + 100*bananicity
contour2 = -ellipse - bananicity*x**2 + 100*bananicity

plt.figure(1)
plt.scatter(samples[:, 0], samples[:, 1], 1, 'red')
plt.plot(x, contour1, 'b-')
plt.plot(x, contour2, 'b-')
plt.xlim([-50, 50])
plt.ylim([-60, 20])

#plt.figure(2)
#plt.xlim([-50, 50])
#plt.ylim([-60, 20])
#x = np.linspace(-50, 50, 100)
#y = np.linspace(-60, 20, 100)
#X, Y = np.meshgrid(x, y)
#logf = np.zeros([100, 100])
#U = np.zeros([100, 100])
#V = np.zeros([100, 100])
#for i, x_i in enumerate(x):
#    for j, y_j in enumerate(y):
#        logf[j, i] = target.log_pdf(np.array([x_i, y_j]))
#        grad = target.log_pdf_gradient(np.array([x_i, y_j]))
#        U[j, i] = grad[0]
#        V[j, i] = grad[1]
#
#levels = np.linspace(-1000, 0, 7)
#plt.contourf(X, Y, logf, levels=levels)
#plt.colorbar()
#plt.quiver(X[::3, ::3], Y[::3, ::3], U[::3, ::3], V[::3, ::3])

plt.show()

