import sys
import matplotlib.pyplot as plt
import math
import cosmocalc

SAVEFOLDER = "Graphs/"

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Given a set of galaxy files, whether from the simulation or otherwise.\n\
    Plots the SEDs for a clear vizualization\n\
    \n\
    python3 Plot_magn.py sim_file1 ... sim_filen -o other_file1 ...\n\n")
    sys.exit()


def get_number( file_name):
    TEMPLATE = "file_"
    file_name = file_name.split("/")[-1]
    number_index = file_name.find(TEMPLATE) + len(TEMPLATE)
    if number_index == len(TEMPLATE) -1:
        return file_name
    number = 0
    while file_name[number_index].isdigit():
        number*=10
        number+= int(file_name[number_index])
        number_index +=1
    return str(number)

###################################################################
#
#          TRANSFORMATION FUNCTION
#
###################################################################


def calculate_shift( value, redshift, dist, modulus_distance):
    if dist == -1:
        dist = (cosmocalc.cosmocalc(redshift, H0=70.4, WM=0.2726, WV=0.7274))['DL_Mpc']
        dist *= 1e6
        modulus_distance = 5.0*(math.log10(dist) - 1.0)
    
    value = 23.9 - 2.5* math.log10(value)
       #Into AB mag from microJks
    value -= modulus_distance 
       #Into absolute magnitude
       
    return value


###################################################################
#
#          GET DATA FILES
#
###################################################################


files_data = []
files_names_sim = []
files_names_other = []
sign = False
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-o":
        sign = True
    else if sign:
        files_names_other.append(sys.argv[i])
    else:
        files_names_sim.append(sys.argv[i])

###################################################################
#
#          GET VALUES
#
###################################################################

C = 1

dist = -1
modulus_distance = -1
redshift = -1
names = []
for i in range(len(files_names_sim)):
    print("Getting Data (SIM) from: "+str(files_names_sim[i]))
    names.append(get_number(files_names_sim[i])
    data_temp = [[], [], []]
    temp_file = open(files_names_sim[i], 'r')
    for line in temp_file:
        values = line.split(' ')
        
        data_temp[0].append(float(values[0]))
        data_temp[1].append(float(values[1]))
        data_temp[2].append(0)
    
    files_data.append(data_temp)
    redshift = -1
    dist = -1

for i in range(len(files_names_other)):
    print("Getting Data (OTH) from: "+str(files_names_other[i]))
    data_temp = [[], [], []]
    temp_file = open(files_names_other[i], 'r')
    names.append(get_number(files_names_other[i])
    for line in temp_file:
        values = line.split(' ')
        
        if len(values) == 1:
            redshift = float(values[0])
        if len(values)>=2:
            data_temp[0].append(float(values[0])/(1+redshift))
            data_temp[1].append(C*calculate_shift(float(values[1]), redshift, dist, modulus_distance))
            data_temp[2].append( C*2.5 * float(values[2])/float(values[1]))
    
    files_data.append(data_temp)
    redshift = -1
    dist = -1


plt.xscale("log")
plt.xlabel("Wavelength")
plt.ylabel("Magnitude")
plt.gca().invert_yaxis()
for i in range(len(files_data)):
    plot_type = "-"

    plt.plot(files_data[i][0], files_data[i][1], plot_type, label=get_number(names[i]))
graph_name = ""
for i in range(len(names)):
    graph_name += get_number(names[i]) + "_"
graph_name +=".png"
print(graph_name)

plt.axis(ymin = 0)

plt.legend(loc = 'lower right')

plt.savefig(SAVEFOLDER + name)
plt.show()
        
