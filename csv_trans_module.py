#-*- coding: UTF-8 -*-
import pandas as pd
import termopare_converter_module as tc

def read(myfile,drawgraph=False): #example: 's14\\a', 's14a'
    
    if myfile.find('\\') == -1:
        end = myfile[-1]
        myfile = myfile[:-1] + '\\' + end
    filename = 'directlog\csv\\' + myfile + '.csv'
    
    src = pd.read_csv(filename, header=None)
    volts = src[1].values.tolist()
    
    clist = []
    for volt in volts:
        mv = volt*1000000
        clist.append(round(mv))
    
    midl = tc.main(clist)
    print(midl)
    
    if(drawgraph == True):
        import matplotlib.pyplot as plt
        plt.plot(midl)
        plt.title(myfile)
        plt.xlabel('t, 100 мс')
        plt.ylabel('T, °С')
        plt.show()    
    
    return(midl)