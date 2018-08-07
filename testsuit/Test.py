import numpy as np
import matplotlib.pyplot as plt
from os.path import isfile, isdir
from os import listdir
from sys import stderr 

from scipy.stats import ks_2samp
from stats import *



################################
# to do:
# avoid loading multiple times 
# the same sample
################################

class TEST: #Test Environment for Sampling algoriThms
    def __init__(self, pathToSamples=None,pathToReference=None, interface="hepmc",lag=0,fixedsize=None):
        """ Init Test Environment.
        :param pathToSamples   : path to a single sample or a directory with samples.
        :param pathToReference : path to a reference sample. Sample has to be a statistically independent.
        :param interface       : contains instructions to interpret sample files.
        :param lag             :
        :param fixedsize       :
        """
        self.set_interface(interface)
        if pathToReference is not None:
            self.Reference = self.interface.getReference(pathToReference)
        if pathToSamples is not None:
            self.Samples   = self.interface.getSamples(pathToSamples)
 
        self.fixedsize=int(min(self.Samples["size"])/(np.max([lag])+1))
        if fixedsize is not None and self.fixedsize < fixedsize:
                print("fixedsize is set to max:"+str(self.fixedsize))
        elif fixedsize is not None:
            self.fixedsize=int(fixedsize)
        else:
            self.fixedsize=None


        self.nSamples=len(self.Samples)
        self.nVSamples=self.nSamples




        if len(np.shape(self.Reference["sample"])) == 1:
            self.ndim = 1
        else:
            self.ndim = np.shape(self.Reference["sample"])[1]

        self.virtual_lag = False
        self.apply_lag(lag)

    
    def set_interface(self,name):
            components = ["interfaces."+name,name,name] 
            mod = __import__(components[0])
            for comp in components[1:]:
                mod = getattr(mod, comp)
            self.interface = mod

    def apply_lag(self,lag):
        if hasattr(lag, "__len__"):
            self.lag = lag
            if 0 not in lag:
                self.lag.append(0)
            else:
                lag.remove(0)
            nolag = np.zeros(self.nSamples)
            self.Samples = append_field(self.Samples,nolag,"virtual_lag","int64")
            temp = np.empty(len(lag)*self.nSamples,dtype=self.Samples.dtype)
            index = 0
            for sample in self.Samples:
                for l in lag:
                    temp[index]=sample
                    temp[index]["virtual_lag"]=l
                    index +=1
            self.Samples = np.append(self.Samples,temp)
            self.virtual_lag = True
            self.nVSamples=len(self.Samples)


        else:
            self.lag=lag


    # param Limits : list of ints, calculates fraction of sequences with minimum lengths given
    def sequenceLength(self,Limits=[10,25,35,50]):
        seql = []
        seqlf = []
        for sample in self.Samples:
            if self.virtual_lag==True:
                lag = sample["virtual_lag"]+1
            else:
                lag = self.lag+1
            data = self.interface.load(sample["sample"])[::lag][:self.fixedsize]
            seql.append(sequenceLength(data))
            seqlf.append(seqLFraction(seql[-1],Limits))
        self.Samples = append_field(self.Samples,seql,"sequenceLength","O")
        self.Samples = append_field(self.Samples,seqlf,"sequenceLengthFraction","O")

    def  KolmogorowSmirnow(self):
        ks_pvalue = np.empty([self.nVSamples,self.ndim])
        for i,sample in enumerate(self.Samples):
            if self.virtual_lag==True:
                lag = sample["virtual_lag"]+1
            else:
                lag = self.lag+1
            data = self.interface.load(sample["sample"])[::lag][:self.fixedsize]
            for axis in range(self.ndim):
                ks_pvalue[i,axis] = ks_2samp(self.Reference["sample"][:,axis],data[:,axis])[1]
        self.Samples = append_field(self.Samples,ks_pvalue.tolist(),"ks_pvalue","O")

    def chiq(self):
        chiq_pvalue = np.empty(self.nVSamples)
        for i,sample in enumerate(self.Samples):
            if self.virtual_lag==True:
                lag = sample["virtual_lag"]+1
            else:
                lag = self.lag+1
            data = self.interface.load(sample["sample"])[::lag][:self.fixedsize]
            bined_data,e = np.histogramdd(data)
            bined_ref ,e = np.histogramdd(self.Reference["sample"],bins=e)
            bined_ref *=np.sum(bined_data)/np.sum(bined_ref)
            chiq_pvalue[i] = chiq(bined_ref,bined_data)[1] 
        self.Samples = append_field(self.Samples,chiq_pvalue.tolist(),"chiq_pvalue","float64")


    def save(self,filename):
        np.save(filename,self.Samples)









def append_field(recarray, newFild, name, dtype):
    if np.shape(recarray)[0] != np.shape(newFild)[0]:
        print("ValueError: in append_field -  operands could not be broadcast together with shapes "+str(np.shape(recarray))+" "+str(np.shape(newFild)),file=stderr)
    dt = recarray.dtype.descr+[(name,dtype)]
    newrecarray = np.empty(recarray.shape, dtype=dt)
    for n in recarray.dtype.names:
        newrecarray[n] = recarray[n]
    newrecarray[name]=newFild
    return newrecarray
