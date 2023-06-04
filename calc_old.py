import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math

import H_Cu
import Fob_Cu
import Fil_Cu
import Fil_Cu_c
import H_Ti
import Fob_Ti
import Fil_Ti
import Fil_Ti_c


def findsr(side): #Ср.арифм среди одного множества
    count = len(side)
    srrow = []
    for i in range(len(side[0])):
        summ = 0
        for row in side:
            summ += row[i]
        sr = summ/count
        srrow.append(sr)
    return srrow

def sterror(srrow,side): #Ср. квадратичный разброс одного множества
    count = len(side)
    if (count == 1):
        null = []
        for j in range(len(srrow)):
            null.append(0)
        return null
    errors = []
    for i in range(len(srrow)):
        sqsum = 0
        for row in side:
            dif = srrow[i] - row[i]
            sqsum += dif*dif
        error = math.sqrt(sqsum)/(count-1)
        errors.append(error)
    return errors

def exterror(errs):
    count = len(errs)
    errl = []
    for i in range(len(errs[0])):
        errq = 0
        for err in errs:
            errq += err[i]*err[i]
        serr = math.sqrt(errq/count)
        errl.append(serr)
    return errl

def extsr(srpare): #П1+П2
    srl = []
    for i in range(len(srpare[0])):
        summ = 0
        for row in srpare: #Только одна линия в списке
            summ += row[i]
        sr = summ/2
        srl.append(sr)
    return srl

def ancorzero(side):
    newside = []
    for row in side:
        base = row[0]
        newrow = []
        for val in row:
            dt = val - base
            newrow.append(dt)
        newside.append(newrow)
    return newside

def to_grf(pare):#П1+П2,err
    newpare = []
    errpare = []
    for side in pare:
        tfr0 = ancorzero(side)
        sr_ar = findsr(tfr0)
        er = sterror(sr_ar,tfr0)
        #print('тепловой эффект:' + str(a))
        #print('погрешность:' + str(da))
        newpare.append(sr_ar)
        errpare.append(er)
    p1p2 = extsr(newpare)
    
    #print(p1p2)
    err = exterror(errpare)
    #print(err)
    return p1p2,err

def gslice(row,err,num):
    return row[num],err[num]

def joules(myslice,tables):
    newd = []
    newe = []
    for n in range(len(myslice[0])):
        num = myslice[0][n]*tables[n].tpe*tables[n].mass/1000
        nume = myslice[1][n]*tables[n].tpe*tables[n].mass/1000
        newd.append(num)
        newe.append(nume)
    newslice = [newd,newe]
    return newslice

def joules1(slice1,table):
    num = slice1[0]*table.tpe*table.mass/1000
    nume = slice1[1]*table.tpe*table.mass/1000
    return num,nume

def drawgraph(tables,plot,mode='all',title=None):
    plot.set(xlabel='Время (мин)', ylabel='Тепловой эффект (°С)')
    plot.xaxis.set_major_locator(ticker.MultipleLocator(5))
    plot.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    plot.grid(True)
    if (type(tables) != list):
        tables = [tables,]
        plot.legend(['центр','край'],loc="center right")
    if (title == None):
        plot.set_title(tables[0].name, y=0.15, pad=-7)
    else:
        plot.set_title(title, y=0.15, pad=-7)
    
    leggs = []
    for table in tables:
        if (mode in ['all','mid']):
            midpare = [table.p1mid,table.p2mid]
            y1,err1 = to_grf(midpare)
            x = range(len(y1))
            plot.errorbar(x, y1, yerr=err1, capsize = 2, lw=2, ecolor='black')
            leggs.append(table.name + ' (центр)')
            
        if (mode in ['all','edge']):
            edgepare = [table.p1edge,table.p2edge]
            y2,err2 = to_grf(edgepare)
            x = range(len(y1))
            plot.errorbar(x, y2, yerr=err2, capsize = 2, lw=2, ecolor='red')
            leggs.append(table.name + ' (край)')
    plot.legend(leggs,loc="center right")
      
def drawallmid(tables,plot):#not there
    for table in tables:
        mid = table.p1mid
        mid = ancorzero(mid)
        y1 = findsr(mid)
        err1 = sterror(y1,mid)
        x = range(len(y1))
        plot.errorbar(x, y1, yerr=err1, capsize = 2, lw=1, ecolor='black')
        plot.set_title('Сводка', y=0.2, pad=-7)
        plot.grid(True)

def drawslice(tables,num,plot,colors,mode='all'):
    llist = []
    for table in tables:
        llist.append(table.name)
    midlist = []
    merrlist = []
    edgelist = []
    ederlist = []
    for table in tables:
        if (mode in ['all','mid']):
            midpare = [table.p1mid,table.p2mid]
            y1,err1 = to_grf(midpare)
            ys1,yerr1 = gslice(y1,err1,num)
            midlist.append(ys1)
            merrlist.append(yerr1)
            
        if (mode in ['all','edge']):
            edgepare = [table.p1edge,table.p2edge]
            y2,err2 = to_grf(edgepare)
            ys2,yerr2 = gslice(y2,err2,num)
            edgelist.append(ys2)
            ederlist.append(yerr2)
    if (mode in ['all','mid']):
        x = range(len(midlist))
        plot.bar(x,midlist, yerr=merrlist, capsize = 3, color = colors, ecolor='black')
    if (mode in ['all','edge']):
        x = range(len(edgelist))
        plot.bar(x,edgelist, yerr=ederlist, capsize = 3, color = colors, ecolor='black')
    plot.set(ylabel='Тепловой эффект через ' + str(num) + ' мин (°С)')
    plt.xticks(x, llist, rotation=20, horizontalalignment='right', fontsize=9)
    plot.grid(True)

def drawsliceonly(myslice,plot,colors,tables):
    llist = []
    for table in tables:
        llist.append(table.name)
    x = range(len(myslice[0]))
    plot.bar(x,myslice[0], yerr=myslice[1], capsize = 3, color = colors, ecolor='black')   
    plot.set(ylabel='Поглощённая энергия через ' + str(1) + ' мин (Дж)')
    plt.xticks(x, llist, rotation=20, horizontalalignment='right', fontsize=9)
    plot.grid(True)

def printtable(tables):
    print('Образец	Начальная температура(центр),°С	Тепловой эффект(1 мин центр),°С	Тепловой эффект(19 мин центр),°С	Тепловой эффект(19 мин край),°С	Энергия(1 мин),Дж')
    for table in tables:
        midpare = [table.p1mid,table.p2mid]
        y0 = extsr([findsr(midpare[0]),findsr(midpare[1])])
        y1,err1 = to_grf(midpare)
        ys1,yerr1 = gslice(y1,err1,1)
        ys19,yerr19 = gslice(y1,err1,29)
        eng1,eerr1 = joules1([ys1,yerr1],table)

        edgepare = [table.p1edge,table.p2edge]
        y2,err2 = to_grf(edgepare)
        ys2,yerr2 = gslice(y2,err2,1)
        ys29,yerr29 = gslice(y2,err2,29)
        print(table.name + ':	' + str(y0[0]) + '	' + str(ys1) + '	' + str(ys19) + '	' + str(ys29) + '	' + str(eng1))

fig,subplots = plt.subplots(nrows=1,ncols=1,figsize=(11,9))
#fig.legend('asd')

#drawgraph(H_Cu,fig.axes[0])
#drawgraph(Fob_Cu,fig.axes[1])
#drawgraph(Fil_Cu,fig.axes[2])
#drawgraph(Fil_Cu_c,fig.axes[3])
#drawgraph(H_Ti,fig.axes[0])
#drawgraph(Fob_Ti,fig.axes[5])
#drawgraph(Fil_Ti,fig.axes[6])
#drawgraph(Fil_Ti_c,fig.axes[7])

#drawgraph([H_Cu,Fob_Cu,Fil_Cu_c],fig.axes[0],'mid','Сравнение образцов меди')
#drawgraph([H_Ti,Fob_Ti,Fil_Ti_c],fig.axes[0],'mid','Сравнение образцов титана')
#drawgraph([H_Cu,H_Ti],fig.axes[0],'all','')
#drawgraph([Fil_Cu_c,Fil_Ti_c],fig.axes[0],'mid','')

#plt.suptitle('sfnd')
totallst = [H_Cu,Fob_Cu,Fil_Cu,Fil_Cu_c,H_Ti,Fob_Ti,Fil_Ti,Fil_Ti_c]
#clr = np.random.rand(len(totallst), 3)
clr = np.array([[0.8, 0.0, 0.0],
 [0.8, 0.4, 0.0],
 [0.8, 0.4, 0.8],
 [0.8, 0.0, 0.7],
 [0.3, 0.3, 0.8],
 [0.7, 0.3, 0.5],
 [0.6, 0.9, 0.9],
 [0.0 ,0.9, 0.9]])

drawslice(totallst,1,fig.axes[0],clr,'mid')
#drawslice(totallst,3,fig.axes[9],clr,'mid')
#drawslice(totallst,29,fig.axes[0],clr,'mid')

#drawallmid(totallst,fig.axes[0])

#midlist = []
#merrlist = []
#for table in totallst:
    #mid = table.p1mid
    #mid = ancorzero(mid)
    #y1 = findsr(mid)
    #err1 = sterror(y1,mid)
    #ys1,yerr1 = gslice(y1,err1,1)
    #midlist.append(ys1)
    #merrlist.append(yerr1)
#tempslc = [midlist,merrlist]
#joulslc = joules(tempslc,totallst)
#drawsliceonly(joulslc,fig.axes[0],clr,totallst)

printtable(totallst)


plt.show()




#import H_Cu_diode_2 as temp
#a = ancorzero(temp.p1mid)
#b = ancorzero(temp.p1edge)
#ad = findsr(a)
#derr = sterror(ad,a)
#ab = findsr(b)
#berr = sterror(ab,b)
#x1 = range(len(ab))
#x2 = range(len(ad))
#plt.errorbar(x2, ad, yerr=derr, lw=1, ecolor='black')
#plt.errorbar(x1, ab, yerr=berr, lw=1, ecolor='red')
#plt.title(temp.name)
#plt.grid(True)
#plt.show()
