import sys
import glob
from Base import get_number

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n\
    Removes galaxies with mass -inf from the properties file.\
    \n\
    python3 Trim_prop_file.py properties_file\n\n")
    sys.exit()


prop_file_name = sys.argv[1]

###
#
# Get values
#
###

prop_file = open(prop_file_name, "r")

prop = {'id': [], 'logst': [], 'met': []}
for line in prop_file:
    add = True
    pre_val = line.split(" ")
    values = []
    for i in pre_val:
        if not (i == '' or i=='\t' or i==' ' or i == '\n'):
            if i == '-inf':
                add = False
            if i == "0.0":
                add = False
            values.append(i)
    if add:
        prop['id'].append(values[0])
        prop['logst'].append(values[1])
        prop['met'].append(values[2])  
prop_file.close()

###
#
# Print out values
#
###

parts = prop_file_name.split('/')
parts[-1] = "trim_aux_properties.txt"

trim_file_name = ""

for i in parts:
    trim_file_name += i + "/"
trim_file_name = trim_file_name[0:-1]

print("Saved to: ", trim_file_name)

trim_file = open( trim_file_name, "w")
for i in range(len(prop['id'])):
    trim_file.write(prop['id'][i] + " " + prop['logst'][i] +" "+ prop['met'][i] + "\n")

trim_file.close()
