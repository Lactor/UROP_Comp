import sys
import glob
import os
import math
import matplotlib.pyplot as plt

if len(sys.argv) != 3:
    print("ERROR number of arguments incorrect")
    exit

data_folder = sys.argv[1]
output_folder = sys.argv[2]

FILE_SECOND_COLUMN = 4 #Position of the value when the line is split
speed_of_light = 3e8

#CALCULATE THE DISTANCE MODULUS

dist_base_2 = (3.086e17)**2
print(dist_base_2)

data_files = glob.glob(data_folder+"/"+ "*.txt")

have_wl = False
data_wl = []
   #Only need one array with the wavelengths

for file_name in data_files:
    file = open(file_name, "r")
       #Opens File
    data_int = []
    print("FILE: "+file_name)
       #Name of openfile

    for line in file:
        values = line.split(' ')
           #array with the numbers on each line
        if not have_wl:
            data_wl.append(float(values[0]))
            

        new_value = float(values[FILE_SECOND_COLUMN])
           #Luminosity per wavelength
        new_value = new_value * data_wl[len(data_int)]**2/speed_of_light
           #Luminosity per frequency
        new_value = new_value/(4*math.pi*dist_base_2)
           #Luminosity to Flux
       
        #print(new_value)
        new_value = new_value * 1e32   
            #Flux in microJanksys
        #print(new_value)
        new_value = 23.9 - 2.5 * math.log10(new_value)
            #Flux to AB magnitude
        print(new_value)
        
        print(" " )
        data_int.append( new_value)
    
        
    have_wl = True

    #Extract the name of the file only:
    name = file_name.split("/")[-1]
    
    #Check if folder exists, otherwise make it
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    
    output = open(output_folder+"/"+name, "w")

    for i in range(len(data_int)):
        output.write(str(data_wl[i]) + " " + str(data_int[i]) + "\n")
    
print("SUCCESS")
