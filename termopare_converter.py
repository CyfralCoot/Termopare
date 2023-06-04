source = 'file' #file, string     'file' ignores mid, edge mode
mode = 'raw' #edge,mid,raw     new mode
pylist = []
outmode = 'list' #excel, list
drawgraph = True

voltages = [838,1093,1387,1619,1819,1999,2149]

table = [
[0,39,78,117,156,195,234,273,312,352,391],
[391,431,470,510,549,589,629,669,709,749,790],
[790,830,870,911,951,992,1033,1074,1114,1155,1196],
[1196,1238,1279,1320,1362,1403,1445,1486,1528,1570,1612],
[1612,1654,1696,1738,1780,1823,1865,1908,1950,1993,2036],
[2036,2079,2122,2165,2208,2251,2294,2338,2381,2425,2468],
[2468,2512,2556,2600,2643,2687,2732,2776,2820,2864,2909],
[2909,2953,2998,3043,3087,3132,3177,3222,3267,3312,3358],
[3358,3403,3448,3494,3539,3585,3631,3677,3722,3768,3814],
[3814,3860,3907,3953,3999,4046,4092,4138,4185,4232,4279],
[4279,4325,4372,4419,4466,4513,4561,4608,4655,4702,4750],
[4750,4798,4845,4893,4941,4988,5036,5084,5132,5180,5228]] #11 значений

def findtemp(volt):
    for dec in range(len(table)):
        lst = table[dec]
        if ((lst[0] <= volt) and (lst[10] > volt)):
            for i in range(11):
                b = lst[i]
                if (b == volt):
                    return 10*dec + i
                elif (b > volt):
                    a = lst[i-1]
                    diff = volt - a
                    gap = b - a
                    dr = diff/gap
                    temp = 10*dec + i - 1 + dr
                    return temp

def printout(num):
    num = round(num,3)
    if (outmode == 'excel'):
        print(num)
    else:
        pylist.append(num)

def main(src,mode):
    if (mode == 'raw'):
        for voltage in src:
            temp = findtemp(voltage)
            printout(temp)
    
    else:
        if (mode == 'mid'):
            temp = findtemp(src[0])
            printout(temp)
            src = src[1:]
        
        temp1 = findtemp(src[0])
        for voltage in src[1:]:
            temp2 = findtemp(voltage)
            printout(temp1)
            srtemp = (temp1 + temp2)/2
            printout(srtemp)
            temp1 = temp2
        if (mode != 'edge'):
            printout(temp2)
    
    if (outmode == 'list'):
        print(pylist)
    
    if (drawgraph == True):
        import matplotlib.pyplot as plt
        plt.plot(pylist)
        plt.show()

if (source == 'string'):
    main(voltages,mode)
else:
    file = open('transfer.txt','r')
    cnt = 0
    for strg in file:
        if (cnt == 0):
            str1 = eval(strg)
            cnt += 1
            continue
        else:
            str2 = eval(strg)
    main(str1,'mid')
    pylist = []
    main(str2,'edge')