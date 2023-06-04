import power_module as power
import csv_trans_module as csv

#sigma = 5.670367*10**-8
#C_Al_estimated = 0.95*sigma #= 5.329*10**-8


#sample = 'H_Al'
#exps = ['s12c','s12d','s12h','s12i','s14j','s14l','s14m','s14n','s14o','s14p','s14q','s14r']

#sample = 'Fob_Al'
#exps = ['s12j','s12k','s15a','s15b','s15c','s15d','s15e']

#sample = 'H_Cu'
#exps = ['s12b','s13p','s14a','s14b','s14s','s14u']

#sample = 'Fob_Cu'
#exps = ['s12n','s14c','s14e','s14f','s14g','s14h','s14i']

#sample = 'H_Ti'
#exps = ['s12m','s13g','s13q','s15g','s15h','s15i','s15k','s15l']

#sample = 'Fob_Ti'
#exps = ['s12l','s13h','s13j','s15m','s15n','s15o','s15p','s15q']


data = []
for exp in exps:
    data.append(csv.read(exp,False)) #True чтобы смотреть отдельно кривые всех экспериментов

pwr = power.average_derivative(data,sample,True)
print(pwr)



    