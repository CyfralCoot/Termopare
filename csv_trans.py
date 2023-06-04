#-*- coding: UTF-8 -*-
import pandas as pd
import termopare_converter_module as tc


to_temperature = True
drawgraph = True

src = pd.read_csv('directlog\csv\s14\\r.csv', header=None)
volts = src[1].values.tolist()

clist = []
for volt in volts:
    mv = volt*1000000
    clist.append(round(mv))

if to_temperature == True:
    midl = tc.main(clist)
    print(midl)
else:
    print(clist)
    midl = clist

if(drawgraph == True):
    import matplotlib.pyplot as plt
    plt.plot(midl)
    plt.title('')
    plt.xlabel('t, 100 мс')
    plt.ylabel('T, °С')
    plt.show()