
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
[4750,4798,4845,4893,4941,4988,5036,5084,5132,5180,5228]] #11 значений в строке

table_minus = [
[0,39,77,116,154,193,231,269,307,345,383],
[383,421,459,496,534,571,608,646,683,720,757],
[757,794,830,867,904,940,976,1013,1049,1085,1121]]

def findtemp(volt): #нахождение температуры интерполяцией по таблице
    for dec in range(len(table)):
        if(volt >= 0):
            lst = table[dec]
            absvolt = volt
        else:
            lst = table_minus[dec]
            absvolt = -1*volt
        if ((lst[0] <= absvolt) and (lst[10] > absvolt)):
            for i in range(11):
                b = lst[i]
                if (b == absvolt):
                    temp = 10*dec + i
                elif (b > absvolt):
                    a = lst[i-1]
                    diff = absvolt - a
                    gap = b - a
                    dr = diff/gap
                    temp = 10*dec + i - 1 + dr
                else:
                    continue
                if (volt < 0):
                    temp = temp*-1
                return temp

def main(src,mode='raw'):
    pylist = []
    for voltage in src:
        temp = findtemp(voltage)
        num = round(temp,3)
        pylist.append(num)
    
    return pylist

def mid(src):
    pylist = []

    temp = findtemp(src[0])
    num = round(temp,3)
    pylist.append(num)
    src = src[1:]
    temp1 = findtemp(src[0])
    for voltage in src[1:]:
        temp2 = findtemp(voltage)
        num = round(temp1,3)
        pylist.append(num)
        srtemp = (temp1 + temp2)/2
        num = round(srtemp,3)
        pylist.append(num)
        temp1 = temp2

    num = round(temp2,3)
    pylist.append(num)

    return pylist

def edge(src):
    pylist = []
    
    temp1 = findtemp(src[0])
    for voltage in src[1:]:
        temp2 = findtemp(voltage)
        num = round(temp1,3)
        pylist.append(num)
        srtemp = (temp1 + temp2)/2
        num = round(srtemp,3)
        pylist.append(num)
        temp1 = temp2

    return pylist    