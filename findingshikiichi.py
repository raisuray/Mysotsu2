import numpy as np
from mymodule.myloader import *

all_res = load_picklefile("all_res_distance_.lst")
all_res = np.array(all_res)

x = 0.01
quar = []
while True:

    val = np.quantile(all_res, x)
    x += 0.01
    quar.append(val)
    if(x >= 0.5):
        break

print(quar)
print(len(quar))
gap = 0
index2 = 0
index1 = 0
for i in range(len(quar)-1):
    temp = quar[i+1] - quar[i]
    print(temp, i+1, i)
    if(temp >= gap):
        gap = temp
        index2 = i+1   
        index1 = i

print(index2, index1)