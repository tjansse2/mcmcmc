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
nsamples = 20
start = np.array([0., 10.])

mu = np.array([0., 0.])
cov = np.array([[.00001, 0.], [0., .00001]])
proposal = Gaussian(mu=mu, cov=cov)
sampler = StaticMetropolis(ndim, target.pdf, proposal)

samples, mean, variance = sampler.sample(nsamples, start)

print(samples)
plt.plot(samples[:, 0], samples[:, 1])


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

