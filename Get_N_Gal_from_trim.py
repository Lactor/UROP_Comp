import sys
import glob
import shutil
from Base import get_number

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Fetches the files of the first N galaxies from the trimmed properties files, generates the properties file and saves everything onto the target_folder\n\
    \n\
    python3 Get_N_Gal_from_trim.py data_folder N trimmed_file target_folder target_properties_folder\n\n")
    sys.exit()

if len(sys.argv) != 6:
    sys.exit("NOT ENOUGH ARGUMENTS")


data_folder = sys.argv[1]
if data_folder[-1] != '/':
    data_folder += '/'
N = int(sys.argv[2])
trimmed_file_name = sys.argv[3]
target_folder  = sys.argv[4]
target_properties_folder = sys.argv[5]

galaxy_id = []

    
###
#
# Get properties from file
#
###

prop_file = open(trimmed_file_name, "r")
prop = {'id': [], 'logst': [], 'met': []}
for line in prop_file:
    pre_val = line.split(" ")
    values = []
    
    for i in pre_val:
        if not (i == '' or i=='\t' or i==' ' or i == '\n'):
            values.append(i)

    prop['id'].append(values[0])
    prop['logst'].append(values[1])
    prop['met'].append(values[2])

prop_file.close()

###
#
#  Choosing the galaxies that are available.
#
###

new_prop_file = open(target_properties_folder + "properties.txt" , "w")

number = 0

for i in range(len(prop['id'])):

    mother_file = data_folder + "file_" + str(prop['id'][i]) + ".txt"
    new_file = target_folder + "file_" + str(prop['id'][i]) + ".txt"
    #print(mother_file + "  ->   "+ new_file)
    
    try:
        shutil.copyfile( mother_file, new_file)
        number += 1
        new_prop_file.write(prop['id'][i]+" "+prop['logst'][i]+" "+prop['met'][i])
    except:
        #print("FILE SKIPPED: " + mother_file)
        pass

    if number >= N:
        break
        

new_prop_file.close()


