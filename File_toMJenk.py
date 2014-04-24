
import sys
import glob
import math
import matplotlib.pyplot as plt

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Given a simulation file, transforms the units to microJanksys \n\
    The data is printed on the console.r\n\
    \n\
    python3 File_toMJenk.py input_file\n\n")
    sys.exit()

def get_number( file_name): #Returns the number of the file
    TEMPLATE = "file_"
    number_index = file_name.find(TEMPLATE) + len(TEMPLATE)
    number = 0
    while file_name[number_index].isdigit():
        number*=10
        number+= int(file_name[number_index])
        number_index +=1
    return number

def toMicroJanksys( val):
    return val*10**(-26-6)

FILE_SECOND_COLUMN = 4 #Position of the value when the line is split

input_file_name = sys.argv[1]
input_file = open(input_file_name, 'r')

data = [[], []] #first array wavelengths second intensities

for line in input_file:
    values = line.split(' ')
    
    data[0].append( float(values[0]))
    #print("Main WL Added: " +str(data[0][-1]) )

    data[1].append( toMicroJanksys(float(values[ FILE_SECOND_COLUMN])))
    
    print('{} {}'.format(data[0][-1], data[1][-1] )) 
