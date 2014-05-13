
# using terminal arguments for the input file and the data folder.
import sys
import glob
import math
import numpy as np
import matplotlib.pyplot as plt
import cosmocalc
import Base as B

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Script that runs the comparison between the input files and the simulation files.\n\
    The results are stored in an individual file for each inputed galaxy on the result_folder\n\
    \n\
    python3 Prof_Comp_Bay.py data_folder properties_file result_folder inp_file1 inp_file2 ...\n\n")
    sys.exit()


data_folder = sys.argv[1]
prop_file_name = sys.argv[2]
result_folder = sys.argv[3]
input_file_names = sys.argv[4:]
input_files_data = []

if data_folder[-1] != '/':
    data_folder += '/'
if result_folder[-1] != '/':
    result_folder +='/'

prop = {}

##################################################################
#
#  Open Properties File and get values
#
##################################################################
def loadProperties():

    print("Loading Properties")
    
    prop_file = open(prop_file_name, "r")
    for line in prop_file:
        values = line.split(' ')
        prop[values[0]] = [float(values[1]), float(values[2])]
    prop_file.close()

loadProperties()
###################################################################
#
#           LOAD FILES
#
###################################################################
def LoadFiles():
    print("Loading Input Files")

    doNotAdd = False #For files with problems in the values
    for i in range(len(input_file_names)):
        print(input_file_names[i])
        data = {"red": -1 } 
        #data dictionary redshift - red
        #wavelengths -wl ; flux - fl; error - err
        input_file = open(input_file_names[i], "r")
        redshift = -1
        temp_wl = []
        temp_fl = []
        temp_err = []
        for line in input_file:
            values = line.split(' ')
            if data['red'] ==-1:
                data['red'] = float(values[0])
                #Redshift is the first value of the file
            else:
                if (len(values) ==3 and float(values[1]) >0 and float(values[2]) > 0):
                    temp_wl.append( float(values[0])/(1+data['red']))
                    temp_fl.append( float(values[1]))
                    temp_err.append( float(values[2]))

                elif len(temp_fl)>1 and temp_fl[-1] <= 0:
                    print(values)
                    doNotAdd = True

        if doNotAdd == False:
            data['wl'] = np.array(temp_wl)
            data['fl'] = np.array(temp_fl)
            data['err'] = np.array(temp_err)
            data['num'] = B.get_number(input_file_names[i])

            input_files_data.append(data)
        input_file.close()
        
LoadFiles()
###################################################################
#
#           TRANSFORM INTO ABSOLUTE MAGNITUDES
#
###################################################################
def Transform():

    print("Formating input data to correct units")
    
    for k in range(len(input_files_data)):

        dist = (cosmocalc.cosmocalc( input_files_data[k]['red'], H0=70.4, WM=0.2726, WV=0.7274))['DL_Mpc']
        #Calculate modulus distance
        dist *= 1e6
        #transform into parsecs
        modulus_distance = 5.0 * (math.log10(dist) - 1.0)
        #Calculate modulus distance

        #DEBUG
    #print("DIST: " + str(dist))
    #print("MOD_DIST: " + str(modulus_distance)) 
        #print("FLUX (microJs): " +str(data['fl'][i]))
        
        input_files_data[k]['err'] = 2.5 * input_files_data[k]['err'] / input_files_data[k]['fl']
          #Error from the transformation of luminosity to magnitude
          
        input_files_data[k]['fl'] = 23.9 - 2.5* np.log10(input_files_data[k]['fl'] )
           # Int Into AB magnitude
    
        #print("Apparent AB mag: %.5e" % (input_files_data[k]['fl'][i]))

        input_files_data[k]['fl'] -= modulus_distance 
             #Into absolute magn

        #print('%.5e %.5e'% (input_files_data[k]['fl'][i], input_files_data[k]['err'][i]))
        #print(" ")

Transform()
###################################################################
#
#            LOAD AND COMPARE TO EACH SIMULATION FILE
#
###################################################################

print("Comparing SED with simulation file:")

data_files = glob.glob(data_folder+"/"+ "*.txt")

cumu_mass = np.zeros(len(input_files_data))
cumu_met = np.zeros(len(input_files_data))
cumu = np.zeros(len(input_files_data))

data_comp_wl = []
size_comp_wl = -1

    #only need to keep one wavelength file for all comparison files
have_wl = False

print_one_file = False
print_one_data = False

def Comp(file_name, have_wl):
    data_comp_file = open(file_name, "r")
    data_comp = [] 
    
    for line in data_comp_file:
        values = line.split(' ')
        if not have_wl:
            data_comp_wl.append( float( values[0]))
            #print("FILE WL Added: " +str(data_comp_wl[-1]) )
            
        data_comp.append( float(values[1]))

    if have_wl == False:
        size_comp_wl = len(data_comp_wl)
        have_wl = True

        
    #STAR COMPARISON

    for k in range(len(input_files_data)):
        
        #For each file do a comparison 
        #print(k, " ", input_file_names[k])
        chi_2 = 0
        index = 0
        int_comp = 0
    
        #VECTORIZATION OF DATA # NEEDS WORK (A LOT)
        file_data_fl = np.zeros(np.shape(input_files_data[k]['wl'])[0])
    
    
        for i in range(np.shape(input_files_data[k]['wl'])[0]):
    
            while input_files_data[k]['wl'][i] < data_comp_wl[0]: 
                i+=1          
                print("DATA WL TOO SMALL")
                #we do not have information to calculate these so we skip

            if input_files_data[k]['wl'][i] > data_comp_wl[-1]:
                i = np.shape(input_files_data[k]['wl'])[0]
                print("DATA WL TOO BIG")
                break 
                # we can stop the loop here since the data points cannot be compared

            while (index + 1) < size_comp_wl and data_comp_wl[index +1] <= input_files_data[k]['wl'][i]:
                index+=1
                #choose the correct index to make the comparison

            file_data_fl[i] = (data_comp[index+1]-data_comp[index])/(data_comp_wl[index+1] - data_comp_wl[index])*(input_files_data[k]['wl'][i] - data_comp_wl[index]) + data_comp[index]
            int_comp +=1
            #print(input_files_data[k]['wl'][i], " " , input_files_data[k]['fl'][i], " " , file_data_fl[i])
            
            
        chi_2 = np.sum( (input_files_data[k]['fl'] - file_data_fl)**2/input_files_data[k]['err'])    
        try:
            chi_2 /= int_comp #normalizes the chi_2 by the number of comparisons
        except:
            print(int_comp)
        if int_comp != np.shape(input_files_data[k]['fl'])[0]:
            print("ERRROR NOT ALL COMPARED")
        
        factor = np.exp(-chi_2)
        cumu[k] += factor
        #print(str(B.get_number(file_name)))
        #print( "MASS: ",prop[str(B.get_number(file_name))][0])
        cumu_mass[k] += factor * prop[str(B.get_number(file_name))][0]
        #print( "MET: ",prop[str(B.get_number(file_name))][1])
        cumu_met[k] += factor * prop[str(B.get_number(file_name))][1]
    data_comp_file.close()


for file_name in data_files:
    #Load comparison file to an array
    #Files have already been changed to be in absolute magnitude
    #From there make the comparisons
    #LOAD FILE
    
    print(file_name)
    Comp(file_name, have_wl)
    

###################################################################
#
#               PRINT RESULTS TO FILE
#
###################################################################
print("Calculating Properties")
def Print():
    masses_input = cumu_mass/cumu
    met_input = cumu_met/cumu
    results = open(result_folder + "results.out", "w")
    for i in range(len(input_files_data)):
        results.write( str(input_files_data[i]['num'])+ " "+str(masses_input[i])+" " + str(met_input[i]) + "\n")
    results.close()

Print()

