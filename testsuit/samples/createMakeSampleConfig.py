#!bin/python
import numpy as np

gauss="""{{
    "name": "mc3-gauss_c-{}_w-{}_b-{}",   
    "target": "densities.Camel",
    "target_args": "{{}}",
    "sampler": "mc3_gauss",
    "size": 100000,
    "params": {{
      "initial": ".4",
      "ndim": "2",
      "centers": "[{}, {}]",
      "widths": "[{},{}]",
      "beta" : "{}"
                }},
   "save_all": "True"
	}}"""

hmc="""{{
    "name": "mc3-hmc_c-{}_w-{}_b-{}_m-{}_s-{}_ss-{}",
    "target": "densities.Camel",
    "target_args": "{{}}",
    "sampler": "mc3_hmc",
    "size": 100000,
    "params": {{
      "initial": ".4",
      "ndim": "2",
      "centers": "[{}, {}]",
      "widths": "[{},{}]",
      "beta": "{}",
      "mass": "{}",
      "steps": "{}",
      "step_size": "{}"
    }},
    "save_all": "True"
  }}"""

def getStringVanilla(center,width,beta):
    return gauss.format(round(center,3),width,beta,0+center,1-center,np.sqrt(width),np.sqrt(width),beta)

def getStringhmc(center,width,beta,mass,s,ss):
    return  hmc.format(round(center,3),width,beta,mass,s,ss,0+center,1-center,np.sqrt(width),np.sqrt(width),beta,mass,s,ss)


with open("vanilla.json","w") as f:
    print("[",file=f)
    centers = [0.1,0.2,0.3,1/3,0.4,0.5]
    widths = [0.001,0.005,0.01]
    betas = np.arange(0,1.1,0.1)

    for center in centers:
        for width in widths:
            for beta in betas:
                end = ",\n"
                if center == centers[-1] and width == widths[-1] and beta == betas[-1]:
                    end = "\n"
                print(getStringVanilla(center,width,round(beta,3)),end=end,file=f)
    print("]",file=f)

with open("hmcmc3.json","w") as f:
    print("[",file=f)
    centers = [1/3,0.5]
    widths = [0.005]
    betas = np.arange(0.1,1,0.1)
    masses = [1.1,0.5]
    stepss = [5,10,15,20,25,30]
    step_sizes = np.linspace(0.01,0.5,10)

    for center in centers:
        for width in widths:
            for beta in betas:
                for mass in masses:
                    for steps in stepss:
                        for step_size in step_sizes:
                            end = ",\n"
                            if center == centers[-1] and width == widths[-1] and beta == betas[-1] and mass == masses[-1] and steps == stepss[-1] and step_size == step_sizes[-1]:
                                end = "\n"
                            print(getStringhmc(center,width,round(beta,3),mass,steps,round(step_size,3)),end=end,file=f)
    print("]",file=f)

