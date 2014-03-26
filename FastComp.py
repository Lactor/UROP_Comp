
# using terminal arguments for the input file and the data folder.
import sys
import glob
import math
import matplotlib.pyplot as plt
import cosmocalc


def get_number( file_name): #Returns the number of the file
    TEMPLATE = "file_"
    number_index = file_name.find(TEMPLATE) + len(TEMPLATE)
    number = 0
    while file_name[number_index].isdigit():
        number*=10
        number+= int(file_name[number_index])
        number_index +=1
    return number


input_file_name = sys.argv[1]
input_file = open(input_file_name, 'r')
data_folder = sys.argv[2]


###################################################################
#
#           LOAD FILE
#
###################################################################

data = { 'wl':[], 'fl':[], 'err':[]} #data array
            #wavelengths -wl ; flux - fl; error - err

redshift = -1
for line in input_file:
    values = line.split(' ')
    
    if redshift==-1:
        redshift = float(values[0])
           #Redshift is the first value of the file
    else:
        print(values)
        data['wl'].append( float(values[0])/(1+redshift))
        data['fl'].append( float(values[1]))
        data['err'].append( float(values[2]))


#DEBUG
print(redshift)
for i in range(len(data['wl'])):
    print(str(data['wl'][i]) + " " + str(data['fl'][i]) + " " + str(data['err'][i]))

###################################################################
#
#           TRANSFORM INTO ABSOLUTE MAGNITUDES
#
###################################################################



dist = (cosmocalc.cosmocalc(redshift, H0=70.4, WM=0.2726, WV=0.7274))['DL_Mpc']
   #Calculate modulus distance
dist *= 1e6
   #transform into parsecs
modulus_distance = 5.0 * (math.log10(dist) - 1.0)
   #Calculate modulus distance

#DEBUG
print("DIST: " + str(dist))
print("MOD_DIST: " + str(modulus_distance)) 


for i in range(len(data['wl'])):
    
    print("FLUX (microJs): " +str(data['fl'][i]))

    data['err'][i] = 2.5 * data['err'][i] / data['fl'][i]
          #Error from the transformation of luminosity to magnitude
    
    data['fl'][i] = 23.9 - 2.5* math.log10(data['fl'][i])
         # Int Into AB magnitude
    
    print("Apparent AB mag: " +str(data['fl'][i]))

    data['fl'][i] -= modulus_distance 
         #Into absolute magn

    print(str(data['fl'][i]) + " " + str(data['err'][i]))
    print(" ")


###################################################################
#
#            LOAD AND COMPARE TO EACH SIMULATION FILE
#
###################################################################

data_files = glob.glob(data_folder+"/"+ "*.txt")

result = []

data_comp_wl = []
    #only need to keep one wavelength file for all comparison files

have_wl = False
for file_data in data_files:
    #Load comparison file to an array
    #Files have already been changed to be in absolute magnitude
    #From there make the comparisons

    #LOAD FILE
    data_comp_file = open(file_data, "r")
    data_comp = [] 

    for line in data_comp_file:
        values = line.split(' ')
        if not have_wl:
            data_comp_wl.append( float( values[0]))
            #print("FILE WL Added: " +str(data_comp_wl[-1]) )
            
        data_comp.append( float(values[1]))
    have_wl = True
    
    #STAR COMPARISON
    chi_2 = 0
    index = 0
    int_comp = 0
    
    for i in range(len(data['wl'])):

        while data['wl'][i] < data_comp_wl[0]: 
            i+=1                     
            #we do not have information to calculate these so we skip

        if data['wl'][i] > data_comp_wl[-1]:
            i = len(data['wl'])
            break 
            # we can stop the loop here since the data points cannot be compared

        while (index + 1) < len(data_comp_wl) and data_comp_wl[index +1] <= data['wl'][i]:
            index+=1
            #choose the correct index to make the comparison
            
        if data_comp_wl[index] == data['wl'][i]: #NO INTERPOLATION
            chi_2 += ((data_comp[index]-data['fl'][i])**2)/data['err'][i]
            int_comp +=1

        elif index +1 < len(data_comp_wl):  #LINEAR INTERPOLATION
            interpol = (data_comp[index+1]-data_comp[index])/(data_comp_wl[index+1] - data_comp_wl[index])*(data['wl'][i] - data_comp_wl[index]) + data_comp[index]
            chi_2 += ((data['fl'][i] - interpol)**2)/data['err'][i]
            int_comp +=1
        else:
            print("BUG OCCURED") #SHOULD NEVER HAPPEN
        
    chi_2 /= int_comp #normalizes the chi_2 by the number of comparisons
    result.append( [chi_2, file_data])


###################################################################
#
#               PRINT RESULTS TO FILE
#
###################################################################


output = open("Results/"+str(get_number(input_file_name)) + ".out", "w") 
   #Open file

for i in range(len(result)):
    output.write(str(get_number(result[i][1])) + " " + str(result[i][0])+"\n")

result.sort()
   #Sorts results for graphing


###################################################################
#
#               MAKE PLOTS
#
###################################################################

epsilon = 0.3

plotdata = [[], []]
for i in range(len(result)):
    plotdata[0].append(get_number(result[i][1]))
    plotdata[1].append(result[i][0])

plt.bar(plotdata[0], plotdata[1], linewidth = 1.0, bottom = 1, color = "blue")
plt.title("Chi^2 of the various files")
plt.xlabel("File Number")
plt.ylabel('Chi^2 of the comparison')
plt.yscale("log")
plt.axis([0,100, 1, max(plotdata[1])*(1+epsilon)])
plt.savefig("Bar/Bar_File_"+str(get_number(input_file_name)) + ".png")
#plt.show()


plt.hist(plotdata[1], 20)
plt.title("Chi^2 of the various files")
plt.ylabel("Number of galaxies")
plt.xlabel('Chi^2 of the comparison')
plt.savefig("Hist/Hist_File_"+str(get_number(input_file_name)) + ".png")
#plt.show()


print("Best few")
for i in range(4):
    print(str(get_number(result[i][1])) + " -> " + str(result[i][0])+"\n")
    
print("Worse few")
for i in range(4):
    print(str(get_number(result[-(1+i)][1])) + " -> " + str(result[-(i+1)][0])+"\n")

