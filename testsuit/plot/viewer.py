import numpy as np
import matplotlib.pyplot as plt

from plot.extract import extract
from plot.plot2d import plot_2d

def view_parm2D(filenameOrData,varZ,varX,varY,varFixed=None,nameX=None,nameY=None,nameZ=None,title=None, critical=None):

    if nameX is None:
        nameX = varX
    if nameY is None:
        nameY = varY
    if nameZ is None:
        nameZ = varZ
    if title is None:
        title = varZ

    if type(filenameOrData) is str:
        filenameOrData = np.load(filename)
    
    matrix,xticks,yticks = extract(filenameOrData,varZ,varX,varY,varFixed)

    if len(np.shape(matrix)) == 2:
        plot_2d(matrix[:,:],critical,title,varX,varY,nameZ,xticks=xticks,yticks=yticks)
    else:
        for axis in range(np.shape(matrix)[2]):
            plot_2d(matrix[:,:,axis],critical,title+" - axis: "+str(axis),varX,varY,nameZ,xticks=xticks,yticks=yticks)

