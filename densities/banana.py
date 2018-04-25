from densities.density_base import Density
from scipy.stats import multivariate_normal
import numpy as np

class Banana(Density):
    def __init__(self, bananicity=0.1):
        self.b = bananicity

    def pdf(self, x):
        if not type(x) is np.ndarray:
            x = np.array(x)
        
        ndim = x.size

        phi = x
        phi[1] = phi[1] + self.b*phi[0]**2 - 100*self.b

        return multivariate_normal.pdf(phi, mean=np.zeros(ndim), cov=[100]+(ndim-1)*[1])
