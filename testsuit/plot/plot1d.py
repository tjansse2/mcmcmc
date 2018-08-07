import numpy as np
import matplotlib.pyplot as plt
from plot.extract import extract

def plot(recarray,varX,varY,*args,varFixed=None, axis=plt,**kwargs):
    y, x = extract(recarray,varY, varX,varFixed)
    return axis.plot(x,y,*args,**kwargs)

