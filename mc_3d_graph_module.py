#-*- coding: UTF-8 -*-
wp1 = 'K:/.minecraft/Profiles/CyfralCoot/1_12/saves/create/'
wp2 = 'data/functions/minecraft/'
way = wp1 + wp2
n1 = 'graph.mcfunction'

cp1 = 'setblock '
block = 'stained_glass'

def mcfg(array):
    mcf = open(way+n1, 'w')
    for point in array:
        coords = point[:-1]
        cp2 = ''
        for num in coords:
            cp2 += '~'
            cp2 += str(num)
            cp2 += ' '
        value = point[3]
        btype = int(3 + value*8)
        command = cp1 + cp2 + block + ' ' + str(btype)
        mcf.write(command+'\n')
    mcf.close()
