# using terminal arguments for the input file and the data folder.
import sys
import glob
import math
import numpy as np
import matplotlib.pyplot as plt
import cosmocalc
import Base as B

SIZE_GAL_FILE = 240

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Script that runs the comparison between the input files and the simulation files.\n\
    The results are stored in an individual file for each inputed galaxy on the result_folder\n\
    \n\
    python3 Bay_MPI.py data_folder properties_file result_folder inp_file1 inp_file2 ...\n\n")
    sys.exit()


data_folder = sys.argv[1]
prop_file_name = sys.argv[2]
result_folder = sys.argv[3]
nGal = len(glob.glob(data_folder+"/"+ "*.txt")))
galaxy_file_data = np.zeros(SIZE_GAL_FILE, nGal)
galaxy_numbers = np.zeros(nGal)
gal_wl = np.zeros(SIZE_GAL_FILE)
input_file_names = sys.argv[4:]

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
    print(prop)

###################################################################
#
#           LOAD FILES
#
###################################################################

def LoadSimFiles():
    print("Loading Simulation Files")
    data_files = glob.glob(data_folder+"/"+ "*.txt")

    for i in range(len(data_files)):
        print(data_files[i])
        gal_file = open(data_files[i], "r")
        index = 0
        for line in gal_file:
            values = line.split(' ')
            if i == 0:
                gal_wl[index] = float(values[0])
            galaxy_file_data[i][index] = float(values[1])
            index+=1
        galaxy_numbers[i] = int(B.get_number(data_files[i]))
        gal_file.close()
        
###################################################################
#
#           TRANSFORM INTO ABSOLUTE MAGNITUDES
#
###################################################################
def Transform( red, data_file, err_file):

    dist = (cosmocalc.cosmocalc( red, H0=70.4, WM=0.2726, WV=0.7274))['DL_Mpc']
        #Calculate modulus distance
    dist *= 1e6
        #transform into parsecs
    modulus_distance = 5.0 * (math.log10(dist) - 1.0)
        #Calculate modulus distance

        #DEBUG
        #print("DIST: " + str(dist))
        #print("MOD_DIST: " + str(modulus_distance)) 
        #print("FLUX (microJs): " +str(data['fl'][i]))
        
    err_file = 2.5 * err_file / data_file
        #Error from the transformation of luminosity to magnitude
        
    data_file = 23.9 - 2.5* np.log10(data_file )
        # Int Into AB magnitude
        
        #print("Apparent AB mag: %.5e" % (input_files_data[k]['fl'][i]))

    data_file -= modulus_distance 
        #Into absolute magn

        #print('%.5e %.5e'% (input_files_data[k]['fl'][i], input_files_data[k]['err'][i]))
        #print(" ")

    return (data_file, err_file)

###################################################################
#
#          CREATE BASE FOR INTERPOLATION
#
###################################################################

def Create_Base(inp_wl):

    index_gl = 0
    index_inp = 0
    base = np.zeros(np.shape(inp_wl)[0])

    while inp_wl[index_inp] < gal_wl[0]: 
        base[index_inp] = -1
        index_inp+=1
        print("ERROR: DATA WL TOO SMALL")
        #we do not have information to calculate these so we skip

    size_inp = np.shape(inp_wl)[0]
    while index_inp<size_inp:

        if inp_wl[index_inp] > gal_wl[-1]:
            base[index_inp] = -2
            index_inp = np.shape(inp_wl)[0]
            print("DATA WL TOO BIG")
            break 
                # we can stop the loop here since the data points cannot be compared

        while (index_gl + 1) < size_inp and gal_wl[index_gl +1] <= inp_wl[index_inp]:
            index_gl+=1
                #choose the correct index to make the comparison

        base[index_inp] = index_gl
        index_inp +=1


    return base.astype(int)


###################################################################
#
# Calculate interpolation
#
###################################################################

def Calculate_Inter(base, inp_wl, gl_index):
    
    size = np.shape(inp_wl)[0]
    interp = np.zeros(size)

    for i in range(size):
        interp[i] = (galaxy_file_data[gl_index][base[i]+1] -galaxy_file_data[gl_index][base[i]])/(gal_wl[base[i]+1] - gal_wl[base[i]])* (inp_wl[i] - gal_wl[base[i]]) + galaxy_file_data[gl_index][base[i]]

    return interp


###################################################################
#
#            LOAD AND COMPARE TO EACH SIMULATION FILE
#
###################################################################

def Comp(file_name):

    print(file_name)
    input_file = open(file_name, "r")
    inp_dat = []
    inp_err = []
    inp_wl = []
    red = -1
    print("Loading data")
    for line in input_file:
        values = line.split(' ')
        if red == -1:
            red = float(values[0])
        
        else:
            if len(values) == 3:
                wl = float(values[0])
                dat = float(values[1])
                err = float(values[2])
                if dat > 0 and err > 0:
                    inp_wl.append(wl)
                    inp_dat.append(dat)
                    inp_err.append(err)
                else:
                    print("Error Quantities less than zero, data ignored" + file_name)
            else:
                print("Error Not enough values " + file_name)
                return -1
    input_file.close()
    inp_wl = np.array(inp_wl)
    inp_dat = np.array(inp_dat)
    inp_err = np.array(inp_err)
    (inp_dat, inp_err) = Transform( red, inp_dat, inp_err)

    #=====================================
    # Star comparison
    #=====================================
    
    print("Creating base")
    base_interpol = Create_Base(inp_wl)

    cumu_mass = 0
    cumu_met = 0
    cumu = 0
    print("Comparing")
    for k in range(len(galaxy_file_data)):

        file_data_fl = Calculate_Inter(base_interpol, inp_wl,k)
            
        chi_2 = np.sum( (inp_dat - file_data_fl)**2/inp_err)    
        
        chi_2 /= np.shape(inp_dat)[0] #normalizes the chi_2 by the number of comparisons
        
        #print(prop[galaxy_file_data[k][0]][0], " ", prop[galaxy_file_data[k][0]][1])
        factor = np.exp(-chi_2)
        cumu += factor
        #print(str(B.get_number(file_name)))
        #print( "MASS: ",prop[str(B.get_number(file_name))][0])
        cumu_mass += factor * prop[galaxy_numbers[k][0]][0]
        #print( "MET: ",prop[str(B.get_number(file_name))][1])
        cumu_met += factor * prop[galaxy_numbers[k][0]][1]

    return (cumu_mass/cumu, cumu_met/cumu)


###################################################################
#
#        Run Code
#
###################################################################


loadProperties()
LoadSimFiles()

results = open(result_folder + "results.out", 'w')

for i in range(len(input_file_names)):
    p = Comp(input_file_names[i])
    
    if p == -1:
        continue
    else:
        name = B.get_number(input_file_names[i])
        results.write(str(name) + " " +str(p[0]) + " " + str(p[1]) + "\n")

results.close()
    
