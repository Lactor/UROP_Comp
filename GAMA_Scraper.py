import urllib.request
import sys
import os.path

if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("\n \
    Given an input file from the GAMA query, automatically downloads the fits files and the other properties.\n \
    They are saved into output folder, with the name ID#.fit and properties, the fit files and the properties respectively \n \
    \n \
    python3 GAMA_Scraper.py input_file output_folder\n\n")
    sys.exit()

if len(sys.argv) != 3:
    sys.exit("ERROR: Wrong number of arguments")
    
input_file_name = sys.argv[1]
output_folder = sys.argv[2]

if output_folder[-1] != '/':
    output_folder += '/'

def isNumber(g):
    if (g>='0' and g<= '9'):
        return True
    else:
        return False


def find_param( name, html):
    index = html.find(name)
    nLines = 0

    #gets line of the value of the param
    while nLines<8:
        if html[index] == '\\' and html[index+1] == 'n':
            nLines+=1
        index+=1

    #gets the position of the value in the string
    start = -1
    stop = False
    while not stop:
        index += 1
        if start == -1 and isNumber(html[index]):
            start = index
        if start != -1 and not isNumber(html[index]) and html[index] != '.':
            stop = True
    #print(start, " ", index, " : ", html[start:index])
    
    value = float(html[start:index])
    return value

input_file = open(input_file_name, "r")
galaxyList = []

#Get the galaxies to scrap
for line in input_file:
    if isNumber(line[0]):
        values = line.split('\t')
        #print(values[0])
        galaxyList.append(values[0])

#print(galaxyList)

#Scrap each galaxy

MAIN_URL = 'http://www.gama-survey.org/dr2/tools/sov.php?cataid='
MASS_URL = 'http://www.gama-survey.org/dr2/tools/querytab.php?tab=StellarMasses&cataid='

massFile = open(output_folder + "properties.txt", "w")
properties = ['logmstar', 'dellogmstar', 'logage', 'dellogage', 'logtau', 'dellogtau', 'metal', 'delmetal']


for galaxy in galaxyList:
    print("Looking at galaxy: " + galaxy)
    galaxyProp = {'num': -1, 'logmstar': -1}
    #Get the value of the Mass
    response = urllib.request.urlopen( MASS_URL + galaxy)
    html = response.read()
    
    #index of reference to stellar mass
    html = str(html)
   
    #Get information
    galaxyProp['num'] = galaxy
    for prop in properties:
        galaxyProp[prop] = find_param(prop, html)
    
    

    #Save information
    info = str(galaxyProp['num'])
    for prop in properties:
        info +=" " + str(galaxyProp[prop])
    print(info)
    info = info[0:-1]
    info += "\n"

    massFile.write(info)

    #########
    # Download file
    #########
    
    #only download if not already present
    if False and not os.path.isfile(output_folder + galaxy+".fit"):
        response = urllib.request.urlopen(MAIN_URL + galaxy)
        html = str(response.read())
        
        template = '<td><a class="nodec" href="'
        index = html.find(template) + len(template)

        downloadUrl = ""
        while html[index] != '"':
            downloadUrl += html[index]
            index +=1
    
        print("Downloading File")
        urllib.request.urlretrieve(downloadUrl, output_folder + galaxy+".fit")
        print("File Downloaded")


print("COMPLETE")
