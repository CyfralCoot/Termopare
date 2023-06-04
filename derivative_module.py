
    
def derivative(myarr):
    d_arr = []
    prev = myarr[0]
    for val in myarr:
        d_arr.append(val - prev)
        prev = val
    return d_arr

def smooth(myarr,count):
    act = []
    qsm = []
    for val in myarr:
        if (len(act) == count):
            qsm.append(sum(act)/count)
            act.append(val)
            act.__delitem__(0)
        else:
            act.append(val)
            qsm.append(0)
            continue
    return qsm

def main(myexp,drawgraph=False):
    der = derivative(myexp)
    appr = smooth(der,50)
    if(drawgraph == True):
        import matplotlib.pyplot as plt
        plt.plot(der)
        plt.plot(appr)
        plt.show()
    return appr