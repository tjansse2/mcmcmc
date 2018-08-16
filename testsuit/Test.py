import numpy as np
import matplotlib.pyplot as plt
from os.path import isfile, isdir
from os import listdir
from sys import stderr 

from scipy.stats import ks_2samp
from stats import *

try:
    from tqdm import tqdm
except ImportError:
     print("tqdm not installed")
     def tqdm(whatever,*args,**kwargs):
         return whatever




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

        if len(np.shape(self.Reference["sample"])) == 1:
            self.ndim = 1
        else:
            self.ndim = np.shape(self.Reference["sample"])[1]

        self.nSamples=len(self.Samples)
        self.applyLag(lag)

    
    def set_interface(self,name):
            components = ["interfaces."+name,name,name] 
            mod = __import__(components[0])
            for comp in components[1:]:
                mod = getattr(mod, comp)
            self.interface = mod

    def applyLag(self,lag):
        if hasattr(lag, "__len__"):
            self.lag = lag
            if 0 not in lag:
                self.lag.append(0)

            nolag = np.zeros(self.nSamples)
            self.Samples = append_field(self.Samples,nolag,"virtual_lag","int64")

            temp = np.empty(len(self.lag),dtype=np.ndarray)
            for i in range(len(temp)):
                temp[i]=self.Samples.copy()
                if i != 0:
                    temp[i]["virtual_lag"] = np.ones(self.nSamples)*self.lag[i]


            self.Samples = temp
            self.nlags = len(self.lag)
        else:
            self.lag=[lag]
            self.Samples = [self.Samples]
            self.nlags=1


    def KolmogorowSmirnow(self,data):
        p_axis = []
        for axis in range(self.ndim):
            p_axis.append(ks_2samp(self.Reference["sample"][:,axis],data[:,axis])[1])
        return p_axis

    def chiq(self,data):
        bined_data,e = np.histogramdd(data)
        bined_ref ,e = np.histogramdd(self.Reference["sample"],bins=e)
        # norm reference
        bined_ref *= np.sum(bined_data)/np.sum(bined_ref)
        return chiq(bined_ref,bined_data)[1] 

    def startTesting(self,chiq=True,ks=True,seqLength=True, Limits=[10,25,35,50]):
        if chiq:
            chiq_pvalue = np.empty([self.nSamples,self.nlags])
        if ks:
            ks_pvalue = np.empty([self.nSamples,self.nlags],dtype=np.ndarray)
        if seqLength:
            seql = np.empty([self.nSamples,self.nlags],dtype=list)
            seqlf = np.empty([self.nSamples,self.nlags],dtype=list)
            seqlfLimits = np.empty([self.nSamples,self.nlags],dtype=list)


        for i_sample,sample_path in tqdm(enumerate(self.Samples[0]["sample"]),total=self.nSamples):
            for i_lag, lag in enumerate(self.lag):
                data = self.interface.load(sample_path)[::lag+1][:self.fixedsize]

                if chiq:
                    chiq_pvalue[i_sample,i_lag] = self.chiq(data)

                if ks:
                    ks_pvalue[i_sample,i_lag] = self.KolmogorowSmirnow(data)

                if seqLength:
                    seql[i_sample,i_lag] = sequenceLength(data)
                    if Limits is not None:
                        seqlf[i_sample,i_lag] = seqLFraction(seql[i_sample,i_lag],Limits)
                        seqlfLimits[i_sample,i_lag] = Limits

        for i_lag in range(self.nlags):
            if chiq:
                self.Samples[i_lag] = append_field(self.Samples[i_lag],chiq_pvalue[:,i_lag],"chiq_pvalue",dtype=float)
            if ks:
                self.Samples[i_lag] = append_field(self.Samples[i_lag],ks_pvalue[:,i_lag],"ks_pvalue",dtype=list)
            if seqLength:
                self.Samples[i_lag] = append_field(self.Samples[i_lag],seql[:,i_lag],"sequenceLength",dtype=list)
                if Limits is not None:
                    self.Samples[i_lag] = append_field(self.Samples[i_lag],seqlf[:,i_lag],"seqLFraction",dtype=list)
                    self.Samples[i_lag] = append_field(self.Samples[i_lag],seqlfLimits[:,i_lag],"seqLFractionLimits",dtype=list)





    def write(self,filename):
        temp = self.Samples[0]
        for sample in self.Samples[1:]:
            temp = np.append(temp,sample) 
        np.save(filename,temp)


def append_field(recarray, newFild, name, dtype):
    if np.shape(recarray)[0] != np.shape(newFild)[0]:
        print("ValueError: in append_field -  operands could not be broadcast together with shapes "+str(np.shape(recarray))+" "+str(np.shape(newFild)),file=stderr)
    dt = recarray.dtype.descr+[(name,dtype)]
    newrecarray = np.empty(recarray.shape, dtype=dt)
    for n in recarray.dtype.names:
        newrecarray[n] = recarray[n]
    newrecarray[name]=newFild
    return newrecarray
