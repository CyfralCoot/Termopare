
file = open('transfer.txt','r')
#file2 = open('lists.txt','w')

templist = []

#print(file[0])
for strg in file:
    try:
        num = float(strg[:-1])
        num = round(num,3)
        templist.append(num)
    except:
        continue

print(templist)
#strl = str(templist)
#file2.write(strl + '\n')

file.close()
#file2.close()