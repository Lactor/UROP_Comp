# using terminal arguments for the input file and the data folder.
import sys
import glob
import math
import numpy as np
import matplotlib.pyplot as plt
import cosmocalc
import Base as B
from mpi4py import MPI


SIZE_GAL_FILE = 240
FILE_SECOND_COLUMN = 4 #Position of the value when the line is split
speed_of_light = 3e8
dist_base_2 = (3.086e17)**2

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
   print(" MPI IMPLEMENTATION OF Baysean interference for the galaxy fittin")
   sys.exit()


data_folder = sys.argv[1]
prop_file_name = sys.argv[2]
result_folder = sys.argv[3]

nGal = len(glob.glob(data_folder+"/"+ "*.txt"))
localgalaxy_numbers = np.zeros(nGal)
galaxy_numbers = np.zeros(nGal)
localgalaxy_file_data = np.zeros( (nGal, SIZE_GAL_FILE) )
galaxy_file_data = np.zeros( (nGal, SIZE_GAL_FILE) )
local_gal_wl = np.zeros(SIZE_GAL_FILE)
gal_wl = np.zeros(SIZE_GAL_FILE)

input_file_names = sys.argv[4:]

if data_folder[-1] != '/':
    data_folder += '/'
if result_folder[-1] != '/':
    result_folder +='/'

local_prop = np.zeros( (3, nGal ))
global_prop = np.zeros( (3, nGal) )
prop = {}

local_results = np.zeros( (3, len(input_file_names) ) )
global_results = np.zeros( ( 3, len(input_file_names) ))
##################################################################
#
#  Open Properties File and get values
#
##################################################################
def loadProperties():

    print("Loading Properties")
    
    prop_file = open(prop_file_name, "r")

    for index,line in enumerate(prop_file):		### HACK.  Needs to be fixed.
        values = line.split(' ')
        local_prop[0][index] = float(values[0])
        local_prop[1][index] = float(values[1])
        local_prop[2][index] = float(values[2])
	if index == (nGal - 1):
	    break

    prop_file.close()
    print(prop)

###################################################################
#
#           LOAD FILES
#
###################################################################

def LoadSimFile( data_file, gal_num):
    
    print(data_file)
    gal_file = open(data_file, "r")
    
    temp_var = np.zeros(SIZE_GAL_FILE)

    for index, line in enumerate(gal_file):
        values = line.split(' ')
        if local_gal_wl[-1] == 0:
            local_gal_wl[index] = float(values[0])
        temp_var[index] = float(values[1])
    localgalaxy_numbers[gal_num] = int(B.get_number(data_file))
    gal_file.close()

    temp_var = temp_var * (local_gal_wl*local_gal_wl)/speed_of_light
           #Luminosity per frequency
    temp_var = temp_var/(4*math.pi*dist_base_2)
           #Luminosity to Flux
       
        #print(new_value)
    temp_var = temp_var * 1e32   
            #Flux in microJanksys
        #print(new_value)
    #print localgalaxy_file_data.shape
    #print temp_var.shape
    #print localgalaxy_file_data[gal_num].shape
    #print localgalaxy_file_data[gal_num,:].shape
    localgalaxy_file_data[gal_num,:]= 23.9 - 2.5 * np.log10(temp_var[:])
        
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
                wl = float(values[0])/(1+red)
                dat = float(values[1])
                err = float(values[2])
                if dat > 0 and err > 0:
                    inp_wl.append(wl)
                    inp_dat.append(dat)
                    inp_err.append(err)
                else:
                    if rank==0:
			print("Error Quantities less than zero, data ignored" + file_name)
            else:
		if rank==0:
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

	#print str(int(galaxy_numbers[k]))

        cumu_mass += factor * prop[str(int(galaxy_numbers[k]))][0]
        #print( "MET: ",prop[str(B.get_number(file_name))][1])
        cumu_met += factor * prop[str(int(galaxy_numbers[k]))][1]

    return (cumu_mass/cumu, cumu_met/cumu)


###################################################################
#
#        Run Code
#
###################################################################

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n_tasks = size
this_task = rank


data_files = glob.glob(data_folder+"/"+ "*.txt")

if this_task ==0:
    loadProperties()

for gal_num, data_file in enumerate(data_files):
    if (gal_num % n_tasks) == rank:
        LoadSimFile( data_file, gal_num)

comm.Barrier()
comm.Allreduce(localgalaxy_numbers, galaxy_numbers, op=MPI.SUM)
comm.Allreduce(localgalaxy_file_data, galaxy_file_data, op=MPI.SUM)
comm.Allreduce(local_gal_wl, gal_wl, op=MPI.SUM)
comm.Allreduce(local_prop, global_prop, op=MPI.SUM)

for i in np.arange(nGal):	#range(len(global_prop)):
#    print i
#    print 'this string is '+str(int(global_prop[0][i]))
    prop[str(int(global_prop[0][i]))] = [global_prop[1][i], global_prop[2][i]]

print("BEGIN COMPARISON")

for i in range(len(input_file_names)):
    if (i%n_tasks) == rank:
        res = Comp(input_file_names[i])
        
        if res == -1: ## Error in running
            continue
        else:
            numb = int(B.get_number(input_file_names[i]))
            local_results[0][i] = numb
            local_results[1][i] = res[0]
            local_results[2][i] = res[1]

comm.Barrier()
comm.Allreduce(local_results, global_results, op=MPI.SUM)

if rank == 0:
    result = open(result_folder + "results.out", "w")
    for i in np.arange(len(global_results[0])):
        result.write(str(global_results[0][i]) + " " + str(global_results[1][i]) + " " + str(global_results[2][i]) + "\n")

    print("SUCCESS")
