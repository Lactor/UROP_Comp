import sys
import numpy as np
import glob
import matplotlib.pyplot as plt
from Base import get_number
import random

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Script that given a set of galaxies, in a folder, gives you the K which divide it.\
    \n\
    python3 K_clustering.py data_folder K\n\n")
    sys.exit()
    

if len(sys.argv) != 3:
    sys.exit("# of arguments wrong")

data_folder = sys.argv[1]
if data_folder[-1] != '/':
    data_folder += '/'
K = int(sys.argv[2])


###
#
# Get data from folder
#
###

wavelengths = []
N_wl = 0
data = []
data_corresp = []
have_wl = False

data_names = glob.glob(data_folder+"*.txt")

for i in data_names:
    data_file = open(i, "r")
    temp = []
    index = 0
    for line in data_file:
        values = line.split(" ")
        if not have_wl:
            wavelengths.append(float(values[0]))
        elif wavelengths[index] != float(values[0]):
            print("ERROR WL NOT EQUAL")
        
        temp.append(float(values[1]))
        index+=1
    
    have_wl = True

    data.append(np.array(temp))
    data_corresp.append(str(get_number(i)))

N_wl = len(wavelengths)

###
#
# Generate randomly the midpoints
#
###

midpoints = []
# for i in range(K):
#     temp = np.random.rand(N_wl)* (-30)
#     midpoints.append(temp)

for i in range(K):
    midpoints.append( data[random.randint(0, len(data)-1)])

print("INITIAL")
print(midpoints)

###
#
# K_clustering Algorithm
#
###

stop_clustering = False

while not stop_clustering:
    
    ##
    #
    # Find closest midpoint for each point
    #
    ##

    closest = np.zeros(len(data))
    n_closest = np.zeros(len(midpoints))
    
    for i in range(len(data)):
        mind = 10**23
        minind = -1

        for o in range(len(midpoints)):
            temp = data[i] - midpoints[o]
            dist = np.dot(temp,temp)
            
            if dist < mind:
                minind = o
                mind = dist

        closest[i] = int(minind)
        n_closest[minind] +=1
        
    ##
    #
    # Shift midpoints to center of closest points
    #
    ##

    prev_mid = []
    
    for i in range(len(midpoints)):
        prev_mid.append(midpoints[i])
        midpoints[i] = np.zeros(N_wl)
    
    
    for i in range(len(data)):
        midpoints[int(closest[i])] += data[i]
    
    for o in range(len(midpoints)):
        midpoints[o] /= n_closest[o]
    
    
    same = True
    for i in range(len(midpoints)):
        if np.all(midpoints[i] != prev_mid[i]) and not( np.all(midpoints[i] != midpoints[i]) or np.all(prev_mid[i] != prev_mid[i])):
            same = False
            break
    
    if same:
        break

print(midpoints)



