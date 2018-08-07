import numpy as np

def extract1D(data,varZ, varX,varFixed=None):                            
    varX_range=np.sort(np.unique(data[varX]))                                                               
    a = np.empty([len(varX_range)],dtype="O")         
                                                                             
    for iX,vX in enumerate(varX_range):                                                                       
        selection =  data[varX]==vX    
        if varFixed!=None:                                               
            for var,value in varFixed:                                   
                selection = np.logical_and(selection,data[var]==value)   
                # print(varX,vX,varY,vY,var,np.sum(selection))
        if sum(selection) != 1:
            print("Selection is not unique")
            print(sum(selection))
            return None
        a[iX] = data[varZ][selection][0]                              
                                                                             
    return np.array(a.tolist()),varX_range

def extract2D(data,varZ, varX, varY,varFixed=None):                            
    varX_range=np.sort(np.unique(data[varX]))                                
    varY_range=np.sort(np.unique(data[varY]))                                
    a = np.empty([len(varX_range),len(varY_range)],dtype="O")         
                                                                             
    for iX,vX in enumerate(varX_range):                                      
        for iY,vY in enumerate(varY_range):                                  
            selection =  np.logical_and(data[varX]==vX,data[varY]==vY)       
            if varFixed!=None:                                               
                for var,value in varFixed:                                   
                    selection = np.logical_and(selection,data[var]==value)   
                   # print(varX,vX,varY,vY,var,np.sum(selection))
            if np.sum(selection) != 1:
                print("Selection is not unique")
                print(np.sum(selection))
                return None
            a[iX,iY] = data[varZ][selection][0]                            
                                                                             
    return np.array(a.tolist()),varX_range,varY_range

def extract(data,varZ, varX, varY=None,varFixed=None):
    if varY is None:
        return extract1D(data,varZ, varX,varFixed)
    else:
        return extract2D(data,varZ, varX, varY,varFixed)
