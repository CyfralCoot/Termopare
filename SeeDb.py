#-*- coding: UTF-8 -*-
import sqlite3 as sql
import numpy as np
import termopare_converter_module as tc

# Открыть или закрыть базу
def BaseConnect(myOpen):
	global conn, curs
	if myOpen:
		conn = sql.connect("expDb.db")
		curs = conn.cursor()
		return True
	else:
		curs.close()
		conn.close()
		return True

def ReadExperiment(myExp):
	global conn, curs
	curs.execute('SELECT value FROM points WHERE expID = ' + str(myExp))
	alist = curs.fetchall()
	#expData = np.array(alist)
	clist = []
	elist = []
	flag = 1
	for val in alist:
		val1 = int(val[0])
		if (flag%2 == 1):
			clist.append(val1)
		else:
			elist.append(val1)
		flag += 1
	midl = tc.main(clist,'mid',True)
	print(midl)
	edgl = tc.main(elist,'edge',True)
	print(edgl)

# MAIN
BaseConnect(True) # открываем базу
ReadExperiment(48)  # Читаем эксперимент
BaseConnect(False) # закрываем базу
