import sys
import matplotlib.pyplot as plt
import math
import cosmocalc

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
files_names = []
index = 100000000
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-o":
        index = len(files_names)
    else:
        files_names.append(sys.argv[i])
print(files_names)
print(index)


###################################################################
#
#          GET VALUES
#
###################################################################


dist = -1
modulus_distance = -1
redshift = -1
for i in range(len(files_names)):
    print("Getting Data from: "+str(files_names[i]))
    data_temp = [[], [], []]
    temp_file = open(files_names[i], 'r')
    print(files_names[i])
    for line in temp_file:
        values = line.split(' ')

        if i < index:
            data_temp[0].append(float(values[0]))
            data_temp[1].append(float(values[1]))
            data_temp[2].append(0)

        else:
            if len(values) == 1:
                redshift = float(values[0])
            if len(values)>=2:
                print(values)
                data_temp[0].append(float(values[0])/(1+redshift))
                data_temp[1].append(calculate_shift(float(values[1]), redshift, dist, modulus_distance))
                data_temp[2].append( 2.5 * float(values[2])/float(values[1]))
    
    files_data.append(data_temp)
    redshift = -1
    dist = -1


plt.xscale("log")
plt.xlabel("Wavelength")
plt.ylabel("Magnitude")
plt.gca().invert_yaxis()
for i in range(len(files_data)):
    plot_type = "-"
    if i>=index:
        plot_type = "o-"
    if files_data[i][2][0] !=0:
        plt.errorbar(files_data[i][0], files_data[i][1], yerr = files_data[i][2])

    plt.plot(files_data[i][0], files_data[i][1], plot_type, label=get_number(files_names[i]))
name = ""
for i in range(len(files_names)):
    name += get_number(files_names[i]) + "_"
name +=".png"
print(name)

plt.axis(ymin = 0)

plt.legend(loc = 'lower right')

plt.savefig(SAVEFOLDER + name)
plt.show()
        
