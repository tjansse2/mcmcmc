#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from densities.banana import Banana
from samplers.mcmc.metropolis import StaticMetropolis
from proposals.gaussian import Gaussian

np.random.seed(1234)

bananicity = 0.1
target = Banana(bananicity)

ndim = 2
nsamples = 100
#start = np.array([0., 10.])
start = np.array([-20., -30.])

mu = np.array([0., 0.])
cov = np.array([[10., 0.], [0., 10.]])
proposal = Gaussian(mu=mu, cov=cov)
sampler = StaticMetropolis(ndim, target.pdf, proposal)

samples, mean, variance = sampler.sample(nsamples, start)

n_accepted = 1
for i in range(1, nsamples):
    if (samples[i] != samples[i-1]).any():
            n_accepted += 1

print('Acceptance rate:', n_accepted/nsamples)
plt.scatter(samples[:, 0], samples[:, 1], 1, 'red')


a = np.sqrt(599)
b = np.sqrt(5.99)
x = np.linspace(-a, a, 200)
ellipse = b/a*np.sqrt(a**2-x**2)
contour1 = ellipse - bananicity*x**2 + 100*bananicity
contour2 = -ellipse - bananicity*x**2 + 100*bananicity

#plt.contour(X, Y, f)
plt.plot(x, contour1, 'b-')
plt.plot(x, contour2, 'b-')
plt.xlim([-50, 50])
plt.ylim([-60, 20])
plt.show()

