import numpy as np
import matplotlib.pyplot as plt
from plot.extract import extract
from plot.viewer import view_parm2D

# Load Data

gauss = np.load("Results/gauss.npy")

# plot 1D

f, (axes) = plt.subplots(2, 3 ,figsize=(15,10))
axes = np.reshape(axes,6)

lag = 0 # no influence on effectiv sample size ( not yet implemented )
for i,center in enumerate(np.unique(gauss["center"])):
    for width in np.unique(gauss["width"]):
        y,x = extract(gauss,"effective_sample_size","beta",varFixed=[("center",center),("width",width),("virtual_lag",lag)])
        axes[i].plot(x,y[:,0],label="cov "+str(width))
        axes[i].set_title("gauss - c: "+str(center))
handles, labels = axes[0].get_legend_handles_labels()
f.legend(handles, labels, loc=7)
plt.suptitle("effective sample size")
plt.show()


# view 2D
view_parm2D(gauss,"ks_pvalue","beta","virtual_lag",varFixed=[("center",0.33),("width",0.5)],nameZ="p_value",critical=0.05,title="gauss - ks")

