from densities.density_base import Density
from scipy.stats import multivariate_normal
import numpy as np
from copy import copy

class Banana(Density):
    def __init__(self, bananicity=0.1):
        self.b = bananicity

    def pdf(self, x):
        if not type(x) is np.ndarray:
            x = np.array(x)
        
        ndim = x.size

        phi = copy(x)
        phi[1] = phi[1] + self.b*phi[0]**2 - 100*self.b

        return multivariate_normal.pdf(phi, mean=np.zeros(ndim), cov=[100]+(ndim-1)*[1])

    def log_pdf_gradient(self, x):
        if not type(x) is np.ndarray:
            x = np.array(x)

        ndim = x.size

        if ndim==2:
            return np.array([-100*x[0]-2*self.b*x[0]*(x[1]+self.bb*x[1]**2-100*self.b), 100*self.b-x[1]-self.b*x[1]**2])

        else:
            return NotImplementedError()
