
# using terminal arguments for the input file and the data folder.
import sys
import glob
import math
import matplotlib.pyplot as plt


def get_number( file_name): #Returns the number of the file
    TEMPLATE = "file_"
    number_index = file_name.find(TEMPLATE) + len(TEMPLATE)
    number = 0
    while file_name[number_index].isdigit():
        number*=10
        number+= int(file_name[number_index])
        number_index +=1
    return number



FILE_SECOND_COLUMN = 4 #Position of the value when the line is split

input_file_name = sys.argv[1]
input_file = open(input_file_name, 'r')
data_folder = sys.argv[2]

data = { 'wl':[], 'int':[], 'err':[]} #first array wavelengths second intensities

for line in input_file:
    values = line.split(' ')
    
    data[0].append( float(values[0]))
    #print("Main WL Added: " +str(data[0][-1]) )

    data[1].append( math.log(float(values[ FILE_SECOND_COLUMN])))
          #Data in logspace
data_files = glob.glob(data_folder+"/"+ "*.txt")

result = []

data_comp_wl = []

have_wl = False
for file_data in data_files:
    #Load comparison file to an array
    #From there make the comparisons
    data_comp_file = open(file_data, "r")
    data_comp = [] #only need to keep one wavelength file for all comparison files
    for line in data_comp_file:
        values = line.split(' ')
        if not have_wl:
            data_comp_wl.append( float( values[0]))
            #print("FILE WL Added: " +str(data_comp_wl[-1]) )
            
        data_comp.append( math.log(float(values[FILE_SECOND_COLUMN])))
    have_wl = True
    
    #Do comparison
    chi_2 = 0
    index = 0
    
    for i in range(len(data[0])):

        while data[0][i] < data_comp_wl[0]: #we do not have inform
            i+=1                     #to calculate these so we skip

        if data[0][i] > data_comp_wl[-1]:
            i = len(data[0])
            break # we can break the for loop here

        while (index + 1) < len(data_comp_wl) and data_comp_wl[index +1] <= data[0][i]:
            index+=1
            
        # if get_number(file_data) == 9:
        #     print(str(i) + "   " + str(index))
        #     print("NEW LINE")
       
        if data_comp_wl[index] == data[0][i]:
            #print("EQUAL: " + str(data_comp_wl[index]))
            chi_2 += (data_comp[index]-data[1][i])**2
        elif index +1 < len(data_comp_wl):
                #Linear interpolation
            #print("DIFFERENT: " + str(data_comp_wl[index])+" "+str(data[0][i]))
            interpol = (data_comp[index+1]-data_comp[index])/(data_comp_wl[index+1] - data_comp_wl[index])*(data[0][i] - data_comp_wl[index]) + data_comp[index]
            chi_2 += (data[1][i] - interpol)**2
        else:
            print("SHOULD NOT HAPPEN")
            #print("READ: "+ str(data_comp_wl[i]))
        #else: #Debug
            #print("NOT READ: " + str(data_comp_wl[i]))
    chi_2 /= len(data[0]) #normalizes the chi_2 by the number of data points
    result.append( [chi_2, file_data])

output = open("Results/"+str(get_number(input_file_name)) + ".out", "w") #Code for outputing the chi^2
for i in range(len(result)):
    output.write(str(get_number(result[i][1])) + " " + str(result[i][0])+"\n")

result.sort()



##### PLOT
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

