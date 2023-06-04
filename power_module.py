import derivative_module as der
import math

material_tpe = {'Cu':400,'Al':903.7,'Ti':530.8}
sample_mass = {'H_Cu':5.2040,'Fob_Cu':5.1732,'Fil_Cu':5.0057,'H_Al':1.6204,'Fob_Al':1.4901,'Fil_Al':1.4977,'C_Al':1.6208,'H_Ti':2.9437,'Fob_Ti':2.8939,'Fil_Ti':2.8182}

#import PAl_c
#import PAl_c_edge
#import PH_Cu
#import PFob_Cu
#import PH_Ti
#import PFob_Ti
#import PH_Al
#import PFob_Al

#import PFil_Al

#totallist = [PAl_c,PAl_c_edge,PH_Cu,PFob_Cu,PH_Ti,PFob_Ti,PH_Al,PFob_Al]
#totallist = [PAl_c]
    

def sterror(mylist): #Ср. квадратичный разброс
    count = len(mylist)
    if (count == 1):
        return 0
    avg = sum(mylist)/count
    sqsum = 0
    for val in mylist:
        dif = avg - val
        sqsum += dif*dif
    error = math.sqrt(sqsum)/(count-1)
    error = round(error,6)
    return error

def sampletpe(mymaterial):
    mass = sample_mass[mymaterial]
    
    lst = ['Cu','Al','Ti']
    for element in lst:
        if (element in mymaterial):
            m_tpe = material_tpe[element]
            break
    
    fulltpe = mass*m_tpe/1000
    return fulltpe

def main(mylst): #старый способ с обьектами
    for obj in mylst:
        explst = obj.a06,obj.a04,obj.a02
        powerlist = []
        print(obj.name + ':')
        if (obj.shortname == 'H_Al_'):
            draw = True
        else:
            draw = False
        for exptype in explst:
            maxlist = []
            for exp in exptype:
                appr = der.main(exp,draw)
                maxlist.append(max(appr))

            #print(maxlist)
            err = sterror(maxlist)
            #print(sr)
            fulltpe = obj.tpe*obj.mass/1000
            power = sr*10*fulltpe # (=/0.1)
            err *= fulltpe*10
            power = round(power,3)
            err = round(err,3)
            powerlist.append(power)
            print('pwr = ' + str(power) + ' +- ' + str(err))
            
        #diflist = []
        #for p in powerlist:
            #diflist.append(p/powerlist[0])
        #print(diflist)

def raw(myexp,sample,drawgraph=False):
    appr = der.main(myexp,drawgraph)
    der_max = max(appr)
    xmax = appr.index(der_max) #координата максимума
    
    fulltpe = sampletpe(sample)
    power = der_max*10*fulltpe
    power = round(power,3)
    return power, xmax

def by_x(myexp,sample,mypos):
    appr = der.main(myexp,False)
    x_der = appr[mypos] #производная в данной точке
    
    fulltpe = sampletpe(sample)
    power = x_der*10*fulltpe
    power = round(power,3)
    return power

def average_derivative(myexps,sample,drawgraph=False): #ищем сначала усреднённый график, потом производную, потом максимум
    average = []
    amount = len(myexps)
    for n in range(1200):
        avg = 0
        for exp in myexps:
            avg += exp[n]
        avg = avg/amount
        average.append(avg)
    
    if drawgraph == True:
        import matplotlib.pyplot as plt
        plt.plot(average)
        for exp in myexps:
            plt.plot(exp)
        plt.show()
        
    avgpower,xmax = raw(average,sample,drawgraph) #после нахождения среднего, кидаем его в обычный модуль расчёта
    
    exp_pwr = [] #погрешность
    for exp in myexps:
        exp_pwr.append(by_x(exp,sample,xmax))
    divergence = sterror(exp_pwr)
    
    return avgpower,xmax,divergence