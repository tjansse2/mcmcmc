import json
from os.path import isdir, isfile
from os import listdir
from sys import stderr
import numpy as np

class hepmc:
    """ interface for samples generated with hepmc"""
    notation={"b" : "beta",       # mixing of mc3
              "c" : "center",     # mapping param of importance sampler
              "w" : "width",      # mapping param of importance sampler
              "s" : "steps",      # param of hmc
              "ss": "step_size",  # param of hmc
              "m" : "mass"        # param of hmc
             }
    @staticmethod
    def getSamples(path):
        dir = listdir(path)
        if "sample-data.npy" in dir and "sample.json" in dir:
            with open(path+"/sample.json") as inf:                             
                info = json.load(inf)
                for key in info.keys():
                    if "array" in info[key]:
                        info[key]=info[key][5:]
                    if key == "type" or key == "target":
                        continue
                    
                    if "nan" in info[key] or "inf" in info[key]:
                        info[key] = info[key].replace("inf","np.inf").replace("nan","np.nan")
                    info[key] = eval(info[key])
                info.update({"sample":path+"/sample-data.npy"})
                info.update(getGeneratorConfig(path)) 
                info =  dictToStructuredArray(info)
                return info
        samples = None
        for item in dir:
            if isdir(path+"/"+item):
                sampel = hepmc.getSamples(path+"/"+item)
                if sampel is not None:
                    if samples is None:
                        samples = sampel
                    else:
                        samples = np.append(samples,sampel)
        return samples
       
    @staticmethod
    def getReference(path):
        if not isdir(path):
            print("Reference path is not a dirctory! Maybe wrong iterface.", file=stderr)
            exit()
        dir = listdir(path)
        info = None
        sample = None
        for key in dir:
            if isfile(path+"/"+key):
                if "npy" in key:
                    if info is not None:
                        print("Info", file=stderr)
                        exit() 
                    sample = np.load(path+"/"+key)
                if "json" in key:
                    with open(path+"/"+key) as inf: 
                        info = json.load(inf) 
                        for key in info.keys():
                            if "array" in info[key]:
                                info[key]=info[key][5:]
                            if key == "type" or key == "target":
                                continue 
                            info[key] = eval(info[key])
        if sample is None:
            print("Reference sample file (npy) not found!", file=stderr)
            exit() 
        if info is None:
            print("Reference info file (json) not found!", file=stderr)
            exit()
        info.update({"sample":sample})
        return info

    @staticmethod
    def load(path):
        return np.load(path)

    
def getGeneratorConfig(path):
    if path[-1] == "/":
        path = path[:-1]
    cut = path.split("/")[-1].split("_")
    config = {}
    for substring in cut:
        if "-" not in substring:
            pass
        if len(substring.split("-"))>2:
            print("Name Error in: "+path+"\n"+"Parameter and Value have to be seperated with \"-\" and different Parameters with \"_\"",file=stderr)
            exit()
        param , value = substring.split("-")
        param = hepmc.notation.get(param,None)
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
