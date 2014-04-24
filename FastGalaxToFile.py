import sys
import glob
import os
import math
import matplotlib.pyplot as plt

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Given the fout and cat file from FAST it compiles the SED data into a single file\n\
    First line contains the redshift and the following lines contain the data.\n\
    \n\
    python3 FastGalaxToFile.py cat_file fout_file output_folder\n\n")
    sys.exit()

if len(sys.argv) != 4:
    sys.error("WRONG NUMBER OF ARGUMENTS")

cat_file_name = sys.argv[1]
fout_file_name = sys.argv[2]
output_folder_name = sys.argv[3]
if output_folder_name[-1] != "/":
    output_folder_name += "/"


cat_file = open(cat_file_name, "r")

#Wavelengths of the bands of the Fast File
#Taken from FILTER.RES.v7.info.txt
#Correspond to file hdfn_fs99.cat

wavelengths = [2.9928e-07,4.5573e-07,6.0013e-07,7.9960e-07,1.2289e-06, 1.6444e-06, 2.2124e-06]

fluxes = []

#From the cat files gets the fluxes and its error
for line in cat_file:
    if line[0] == '#':
        continue
    prevalues = line.split(" ")
    values = []
    for i in range(len(prevalues)):
        if not prevalues[i] == '':
            values.append(float(prevalues[i]))
    fluxes.append(values[1:-1])

cat_file.close()

redshifts = []
# From the fout files gets the redshifts
fout_file = open(fout_file_name, "r")
for line in fout_file:
    if line[0] == '#':
        continue
    prevalues = line.split(" ")
    values = []
    for i in range(len(prevalues)):
        if not prevalues[i] == '':
            values.append(float(prevalues[i]))
    redshifts.append(values[1])

fout_file.close()

#Save the information of each file.

if not os.path.isdir(output_folder_name):
    os.mkdir(output_folder_name)

for i in range(len(redshifts)):
    out_file_name = output_folder_name +"gal_" + str(i+1)+".txt"
    out_file = open(out_file_name, "w")
    
    out_file.write(str(redshifts[i]) + "\n")
    
    for o in range(0,len(fluxes[i])-1,2):
        out_file.write('%.5e %.5e %.5e\n' %(wavelengths[int(o/2)], fluxes[i][o] ,fluxes[i][o+1]))
out_file.close()

