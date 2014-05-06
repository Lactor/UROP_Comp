import sys
import matplotlib.pyplot as plt
import math

SAVEFOLDER = "Graphs/"

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Given a set of galaxy files, whether from the simulation or otherwise.\n\
    Plots the SEDs for a clear vizualization\n\
    \n\
    python3 Plot_SED.py sim_file1 ... sim_filen -o other_file1 ...\n\n")
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

FILE_SECOND_COLUMN = 4

files_data = []
files_names_sim = []
files_names_other = []
sign = False
index = 100000000
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-o":
        sign = True
    elif sign:
        files_names_other.append(sys.argv[i])
    else:
        files_names_sim.append(sys.argv[i])


wavelengths = []


for i in range(len(files_names_sim)):
    data_temp = [[], []]
    temp_file = open(files_names[i], 'r')
    print(files_names_sim[i])
    for line in temp_file:
        values = line.split(' ')

        data_temp[0].append(float(values[0]))
        data_temp[1].append(math.log(float(values[FILE_SECOND_COLUMN])))
    files_data.append(data_temp)

for i in range(len(files_names_other)):
    data_temp = [[], []]
    temp_file = open(files_names[i], 'r')
    print(files_names_other[i])
    for line in temp_file:
        values = line.split(' ')
        if len(values)>=2:
            print(values)
            data_temp[0].append(float(values[0]))
            data_temp[1].append(math.log(float(values[1])))

    files_data.append(data_temp)



plt.xscale("log")
plt.xlabel("Wavelength")
plt.ylabel("Intensity")
for i in range(len(files_data)):
    plt.plot(files_data[i][0], files_data[i][1])
name = ""
for i in range(len(files_names)):
    name += get_number(files_names[i]) + "_"
name +=".png"
print(name)
maxX = 0
minX =  10**10

plt.savefig(SAVEFOLDER + name)
plt.show()
        
