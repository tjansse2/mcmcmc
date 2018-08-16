import numpy as np
import matplotlib.pyplot as plt
from plot.extract import extract
from plot.viewer import view_parm2D

# Load Data

gauss = np.load("Results/gauss.npy")
hmc = np.load("Results/hmc.npy")


# plot 1D


lag = 0 # no influence on effective_sample_size ( not yet implemented)
center = 0.333
width = 0.005

f, (axes) = plt.subplots(2, 3, sharey=True,figsize=(15,10))
axes = np.reshape(axes,6)

for i,center in enumerate(np.unique(gauss["center"])):
    for width in np.unique(gauss["width"]):
        y,x = extract(gauss,"effective_sample_size","beta",varFixed=[("center",center),("width",width),("virtual_lag",lag)])
        axes[i].plot(x,y[:,0],label="width "+str(width))
        axes[i].set_title("gauss - c: "+str(center))
handles, labels = axes[0].get_legend_handles_labels()
f.legend(handles, labels, loc=7)
plt.suptitle("effective sample size")
plt.show()



center = 0.333
w = 0.005
lag = 0 # no influence on effectiv sampling size ( not yet implemented )
mass = 1.1
step_size = -1
steps = -1

f, (axes) = plt.subplots(4, 3, sharey=True,figsize=(15,15))
axes = np.reshape(axes,12)

for i,step_size in enumerate(np.unique(hmc["step_size"])):
    for steps in np.unique(hmc["steps"]):
        if i == 9:
            i=10
        y,x = extract(hmc,"effective_sample_size","beta",varFixed=[("center",0.333),("width",0.005),("virtual_lag",lag),("steps",steps),("step_size",step_size),("mass",0.5)])
        axes[i].plot(x,y[:,0],label="steps "+str(steps))
        axes[i].set_title("hmc - c: "+str(center)+ " - w: "+str(w)+" - l: "+str(lag)+" - m: "+str(mass)+ " - ss: "+str(step_size))

handles, labels = axes[0].get_legend_handles_labels()
f.legend(handles, labels, loc=7)
plt.suptitle("effective sample size")
plt.show()

# view 2D
view_parm2D(gauss,"ks_pvalue","beta","virtual_lag",varFixed=[("center",0.333),("width",0.005)],nameZ="p_value",critical=0.05,title="gauss - ks")

view_parm2D(hmc,"ks_pvalue","beta","virtual_lag",varFixed=[("center",0.333),("width",0.005),("mass",1.1),("steps",15),("step_size",0.119)],nameZ="p_value",critical=0.05,title="hmc - ks")

