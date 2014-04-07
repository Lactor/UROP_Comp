import sys
import glob
import os
import math
import matplotlib.pyplot as plt
import pyfits


def get_number( file_name):
    TEMPLATE = "gama_"
    file_name = file_name.split("/")[-1]
    number_index = file_name.find(TEMPLATE) + len(TEMPLATE)
    if number_index == len(TEMPLATE) -1:
        return file_name.split(".")[0]
    number = 0
    while file_name[number_index].isdigit():
        number*=10
        number+= int(file_name[number_index])
        number_index +=1
    return str(number)


if len(sys.argv) != 6:
    sys.error("WRONG NUMBER OF ARGUMENTS")

results_folder_name = sys.argv[1]
if results_folder_name[-1] != "/":
    results_folder_name += "/"

data_folder_name = sys.argv[2]
if data_folder_name[-1] != "/":
    data_folder_name += "/"

sim_mass_name = sys.argv[3]
GAMA_mass_name = sys.argv[4]
output_file = sys.argv[5]

data_extracted = { 'num': [], 'red': [], 'ms': [], 'mf': []}

masses_GAMA = {}

GAMA_mass_file = open(GAMA_mass_name, "r")
for line in GAMA_mass_file:
    if line[0] == '#':
        continue
    values = line.split(" ")
    masses_GAMA[values[0]] = float(values[1])
GAMA_mass_file.close()

print(masses_GAMA)

masses_sim = {}

sim_mass_file = open(sim_mass_name, "r")

for line in sim_mass_file:
    values = line.split(" ")
    masses_sim[values[0]] = float(values[1])

sim_mass_file.close()

print(masses_sim)

results_files = glob.glob(results_folder_name +"gama_*.out")

for result in results_files:
    print(result)
    number = get_number(result)
    data_extracted['num'].append(number)
    redshift_file = pyfits.open(data_folder_name +str(number)+".fit")
    data_extracted['red'].append(float(redshift_file[0].header['z']))
    
    data_extracted['mf'].append(masses_GAMA[number])
    
    result_file = open(result, "r")

    sim_num = -1
    for line in result_file:
        sim_num =str(int(line.split(" ")[0]))
        break
    
    data_extracted['ms'].append(masses_sim[sim_num])

print("%d %d %d %d" %( len(data_extracted['num']), len(data_extracted['red']), len(data_extracted['ms']), len(data_extracted['mf'])))

output = open(output_file, "w")

for i in range(len(data_extracted['num'])):
    output.write("%d %.8e %.8e %.8e\n" % (int(data_extracted['num'][i]), data_extracted['red'][i], data_extracted['ms'][i], data_extracted['mf'][i]))


###################################################################
#
#           LET'S PLAY WITH THE DATA
#
###################################################################

    
#PLOT ms as a function of mf

plt.plot(data_extracted['mf'], data_extracted['ms'], "bo")
plt.plot([9,12], [9,12], "r-")
plt.xlabel("Mass Fast")
plt.ylabel("Mass Sim")
plt.title("Plot of the mass of the simulation as a function of the mass of fast")
plt.savefig("mf_ms.png")
plt.show()


#PLOT difference in mass as a function of redshift

dif = []
for i in range(len(data_extracted['ms'])):
    dif.append(data_extracted['ms'][i] - data_extracted['mf'][i])

plt.plot(data_extracted['red'], dif, "bo")
plt.plot([0,0.45], [0,0], "r-")
plt.xlabel("Redshift")
plt.ylabel("Diference M_sim - M_fast")
plt.title("Plot of the difference in masses as a function of redshift")
plt.savefig("red_dif.png")
plt.show()

