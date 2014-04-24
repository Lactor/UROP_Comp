import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Given a file with the Baysean masses and a file with the Best FiT and GAMA masses.\n\
    Plots graphs that better allow the understanding of the relationships\n\
    \n\
    python3 Plot_BF_Bay.py Best_fit_and_GAMA Baysean_file\n\n")
    sys.exit()



BF_file_name = sys.argv[1]
Bay_file_name = sys.argv[2]

Bay_masses = {}
BF_masses = {}
Gama_masses = {}

NBINS = 100

###
#Load Data from Baysean file
###


Bay_data = open(Bay_file_name, "r")

for line in Bay_data:
    values = line.split(" ")
    print(values)
    if values[1] == "nan\n":
        print(values[0])
        continue
    Bay_masses[values[0]] = float(values[1])

Bay_data.close()


###
#Load BF and Gama masses
###

BF_data = open(BF_file_name, "r")

for line in BF_data:
    values = line.split(" ")
    BF_masses[values[0]] = float(values[2])
    Gama_masses[values[0]] = float(values[3])

###
# Prepare for Plot
###


Bay_array =[]
BF_array = []
Gama_array = []

for i in Bay_masses:
    Bay_array.append(Bay_masses[i])
    BF_array.append(BF_masses[i])
    Gama_array.append(Gama_masses[i])

Bay_array = np.array(Bay_array)
BF_array = np.array(BF_array)
Gama_array = np.array(Gama_array)

plt.hist2d(Bay_array, BF_array, bins = NBINS)
plt.plot([9.5,12],[9.5,12], 'r-')
plt.ylabel("Best fit")
plt.xlabel("Baysean")
plt.colorbar()
plt.savefig("Bay-Best.png")
plt.show()

avg =  np.sum(Bay_array-BF_array)/len(Bay_array)
std =  np.sqrt( np.sum( (Bay_array-BF_array - avg)**2)/len(Bay_array))
print("AVG: " + str(avg))
print("STD: " + str(std))

plt.hist2d( Gama_array,Bay_array-BF_array, bins = NBINS)
plt.plot([5,12],[0,0], "r-")
plt.ylabel("Baysean - Best fit")
plt.xlabel("Gama Mass")
plt.colorbar()
plt.show()


avg =  np.sum(BF_array/Bay_array)/len(Bay_array)
std =  np.sqrt( np.sum( (BF_array/Bay_array - avg)**2)/len(Bay_array))
print("AVG: " + str(avg))
print("STD: " + str(std))


plt.hist2d( Gama_array,BF_array/Bay_array, bins = NBINS)
plt.plot([5,12],[1,1], "r-")
plt.ylabel("Baysean/Best fit")
plt.xlabel("Gama Mass")
plt.colorbar()
plt.show()

plt.hist2d( Gama_array,BF_array, bins = NBINS)
plt.plot([9.5,12],[9.5,12], "r-")
plt.ylabel("Best fit")
plt.xlabel("Gama Mass")
plt.colorbar()
plt.show()

plt.hist2d( Gama_array,Bay_array, bins = NBINS)
plt.plot([9.5,12],[9.5,12], "r-")
plt.ylabel("Baysean")
plt.xlabel("Gama Mass")
plt.colorbar()
plt.show()
