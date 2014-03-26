import sys
import matplotlib.pyplot as plt
import math

SAVEFOLDER = "Graphs/"

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
files_names = []
index = 100000000
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-o":
        index = len(files_names)
    else:
        files_names.append(sys.argv[i])
print(files_names)
print(index)

wavelengths = []

maxY= 0
minY = 10**10

for i in range(len(files_names)):
    data_temp = [[], []]
    temp_file = open(files_names[i], 'r')
    print(files_names[i])
    for line in temp_file:
        values = line.split(' ')

        if i < index:
            data_temp[0].append(float(values[0]))
            data_temp[1].append(math.log(float(values[FILE_SECOND_COLUMN])))

        else:
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

for i in range(len(files_data)):
    maxX = max(maxX, files_data[i][0][-1])
    minX = min(minX, files_data[i][0][0])
#plt.axis([minX, maxX, minY, maxY])
plt.savefig(SAVEFOLDER + name)
plt.show()
        
