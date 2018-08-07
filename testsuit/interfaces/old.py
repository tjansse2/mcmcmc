import json
from os.path import isdir, isfile
from os import listdir
from sys import stderr
import numpy as np

class old:
    """ interface for samples generated with hepmc"""
    notation={"b" : "beta",       # mixing of mc3
              "c" : "center",     # mapping param of importance sampler
              "w" : "with",       # mapping param of importance sampler
              "s" : "steps",      # param of hmc
              "ss": "step_size"   # param of hmc
             }
    @staticmethod
    def getSamples(path):
        dir = listdir(path)
        Samples = None 
        for item in dir:
            if "npy" in item:
                info = np.load(path+"/"+item)[()]
                info.update({"sample":path+"/"+item})
                config = getGeneratorConfig(path+"/"+item)  
                info.update(config)
                info.update({"size":len(info["samples"])})
                del info["samples"]
                print(config)
                info =  dictToStructuredArray(info)
                if Samples is None:
                    Samples = info
                else:
                    Samples = np.append(Samples,info)
        return Samples
       
    @staticmethod
    def getReference(path):
        sample = np.load(path)[()][0]
        return {"sample":sample}

    @staticmethod
    def load(path):
        return np.load(path)[()]["samples"]

    
def getGeneratorConfig(path):
    if path[-1] == "/":
        path = path[:-1]
    if path[-4:] == ".npy":
        path = path[:-4]
    cut = path.split("/")[-1].split("-")
    config = {}
    for substring in cut[1:]:
        if "_" not in substring:
            pass
        if len(substring.split("_"))>2:
            print("Name Error in: "+path+"\n"+"Parameter and Value have to be seperated with \"-\" and different Parameters with \"_\"",file=stderr)
            exit()
        param , value = substring.split("_") 
        if param is None:
            pass
        else:
            config.update({param:float(value)})
    return config
        

def dictToStructuredArray(dict):
    dtypes = []
    for value,key in zip(dict.values(),dict.keys()):
        dtype = str(np.dtype(type(value)))
        if "U" in dtype:
            dtype = "|O"
        dtypes.append((key,dtype))
    return np.array(tuple(dict.values()),dtype=dtypes)
