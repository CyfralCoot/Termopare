import mc_3d_graph_module as mc

#powerIns = k1*tempeffects + sigma*a*t4s

sigma = 5.670367*10**-8
C_Al_estimated = 0.95*sigma #= 5.329*10**-8

#pwr6 = 1.029696/0.000625
#pwr4 = 0.733091/0.000625
#pwr2 = 0.423791/0.000625

#C_Al
#sttmp6 = 20.052
#sttmp4 = 20.7
#sttmp2 = 20.075

#endtmp6 = 80.806
#endtmp4 = 65.048
#endtmp2 = 45.132

#Fob_Cu
#pwr6 = 1.297956/0.000625

#sttmp6 = 26.473
#sttmp4 = 18.95
#sttmp2 = 17.787

#endtmp6 = 82.353
#endtmp4 = 60.409
#endtmp2 = 40.798

#H_Cu
pwr6 = 1.071504/0.000625

sttmp6 = 26.726
sttmp4 = 20.016
sttmp2 = 16.725

endtmp6 = 84.879
endtmp4 = 64.386
endtmp2 = 39.452

def pwrs(inpwr1,sttemp1,sttemp2,endtemp1,endtemp2,myk2):
    tf1 = endtemp1 - sttemp1
    tf2 = endtemp2 - sttemp2
    t41 = (endtemp1+273.15)**4 - (sttemp1+273.15)**4
    t42 = (endtemp2+273.15)**4 - (sttemp2+273.15)**4
    
    del21 = tf2/tf1
    
    inpwr2 = inpwr1*del21 + myk2*(t42 - t41*del21)
    return inpwr2

def cofficients(inpwr1,inpwr2,sttemp1,sttemp2,endtemp1,endtemp2):
    tf1 = endtemp1 - sttemp1
    tf2 = endtemp2 - sttemp2
    t41 = (endtemp1+273.15)**4 - (sttemp1+273.15)**4
    t42 = (endtemp2+273.15)**4 - (sttemp2+273.15)**4
    
    tr1 = inpwr1*tf2/tf1
    tr2 = t41*tf2/tf1 #делим и домножаем обе части уравнения на
    
    wdif = inpwr2 - tr1
    k2dif = t42 - tr2
    
    k2 = wdif/k2dif #Коэффициент теплопередачи излучением
    k1 = (inpwr1 - k2*t41)/tf1 #коэффициент теплопередачи теплопроводностью
    rad_koef = k2/sigma
    return k1,rad_koef

def approximately_eq(myvals):
    bottom = myvals[0]*0.99
    top = myvals[0]*1.01
    for val in myvals:
        if ((val < bottom) or (val > top)):
            return False
    return True

#pwr4 = pwrs(pwr6,sttmp6,sttmp4,endtmp6,endtmp4,C_Al_estimated)
#pwr2 = pwrs(pwr4,sttmp4,sttmp2,endtmp4,endtmp2,C_Al_estimated)
pwr4 = pwr6/1.3972645545364426
pwr2 = pwr6/2.5364260401296894

steps = 30
half = steps/2
#temp4 = sttmp4 + tempval2*0.5
temp2 = sttmp2
temp4 = sttmp4
temp6 = sttmp6
tempval1 = 0
matches = []
for powerval1 in range(steps):
    power6 = pwr6 + (half - powerval1)
    for powerval2 in range(steps):
        power4 = pwr4 + (half - powerval2)
        for powerval3 in range(steps):
            power2 = pwr2 + (half - powerval3)
            
            k1_46,rad_koef_46 = cofficients(power4,power6,temp4,temp6,endtmp4,endtmp6)
            k1_26,rad_koef_26 = cofficients(power2,power6,temp2,temp6,endtmp2,endtmp6)
            k1_24,rad_koef_24 = cofficients(power2,power4,temp2,temp4,endtmp2,endtmp4)
            
            #if ((k1_46 <= 0) or (rad_koef_46 < 0.001) or (rad_koef_46 > 1)):
                #continue
            if (approximately_eq([k1_46,k1_26,k1_24])):
                matches.append([powerval1,powerval2,powerval3,rad_koef_26])
                print(str(powerval1) + ', ' + str(powerval2) + ', ' + str(powerval3))
                print(k1_46,rad_koef_46)
                print(k1_26,rad_koef_26)
                print(k1_24,rad_koef_24)

#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')

print('finished')
best = [None,None,None,(steps*10)**2]
perfect = []
for match in matches:
    distance = 0
    #ax.scatter(xs=match[0], ys=match[1], zs=match[2])
    for val in match[:-1]:
        distance += (half - val)**2
    if (distance <= best[-1]):
        best = match
        best.append(distance)
    if (distance == 0):
        perfect.append(best)
print(best)
print(perfect)

print(f'1, {pwr6/pwr4}, {pwr6/pwr2}')
#1, 1.3972645545364426, 2.5364260401296894

#real 1, 1.426098535286284921, 2.385300668151
#*1.0, 0.7012138188608777, 0.419234360410831

matches.append([half,half,half,0])
#mc.mcfg(matches)

#ax.scatter(xs=half, ys=half, zs=half)
#plt.show()
