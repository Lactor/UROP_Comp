import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Given a file with the Baysean masses and a file with the Best FiT and GAMA masses.\n\
    Plots graphs that better allow the understanding of the relationships\n\
    \n\
    python3 Plot_Bay_Gama.py GAMA_file Baysean_file results_folder\n\n")
    sys.exit()



Gama_file_name = sys.argv[1]
Bay_file_name = sys.argv[2]
SAVEFOLDER = sys.argv[3]
if SAVEFOLDER[-1] != "/":
    SAVEFOLDER+="/"

Bay_masses = {}
Gama_masses = {}
redshifts = {}

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
#Load Gama masses
###

Gama_data = open(Gama_file_name, "r")

for line in Gama_data:
    values = line.split(" ")
    redshifts[values[0]] = float(values[1])
    Gama_masses[values[0]] = float(values[3])

###
# Prepare for Plot
###


Bay_array =[]
Gama_array = []
redshifts_array = []

for i in Bay_masses:
    Bay_array.append(Bay_masses[i])
    Gama_array.append(Gama_masses[i])
    redshifts_array.append(redshifts[i])
    

Bay_array = np.array(Bay_array)
Gama_array = np.array(Gama_array)
redshifts_array = np.array(redshifts_array)


plt.plot(redshifts_array, Bay_array - Gama_array, "bo")
plt.plot([0, 0.6], [0,0], "r-")
plt.ylabel("Bay_Masses - GAMA Masses")
plt.xlabel("Redshift")
plt.title("Plot of the mass difference as a function of the redshift")
plt.savefig(SAVEFOLDER + "diff_red.png")
plt.show()




plt.hist2d( Gama_array,Bay_array, bins = NBINS)
plt.plot([9.5,12],[9.5,12], "r-")
plt.ylabel("Baysean")
plt.xlabel("Gama Mass")
plt.colorbar()
plt.savefig(SAVEFOLDER + "Bay_GAMA.png")
plt.show()

