
# using terminal arguments for the input file and the data folder.
import sys
import glob
import math
import matplotlib.pyplot as plt


def get_number( file_name):
    TEMPLATE = "file_"
    number_index = file_name.find(TEMPLATE) + len(TEMPLATE)
    number = 0
    while file_name[number_index].isdigit():
        number*=10
        number+= int(file_name[number_index])
        number_index +=1
    return number

FILE_SECOND_COLUMN = 4
input_file_name = sys.argv[1]
input_file = open(input_file_name, 'r')
data_folder = sys.argv[2]

data = []

for line in input_file:
    values = line.split(' ')
    data.append( math.log(float(values[ FILE_SECOND_COLUMN])))

data_files = glob.glob(data_folder+"/"+ "*.txt")

result = []

for i in data_files:
    data_comp_file = open(i, "r")
    chi2 = 0
    index = 0
    for line in data_comp_file:
        value = math.log(float(line.split(' ')[FILE_SECOND_COLUMN]))
        chi2 += (data[index] - value)**2
        index +=1
    result.append( [chi2, i])

result.sort()
output = open("results.out", "w")
for i in range(len(result)):
    output.write(str(get_number(result[i][1])) + " " + str(result[i][0])+"\n")



##### PLOT

plotdata = [[], []]
for i in range(len(result)):
    plotdata[0].append(get_number(result[i][1]))
    plotdata[1].append(result[i][0])

plt.bar(plotdata[0], plotdata[1], linewidth = 1.0, bottom = 10**3, color = "blue")
plt.title("Chi^2 of the various files")
plt.xlabel("File Number")
plt.ylabel('Chi^2 of the comparison')
plt.yscale("log")
plt.savefig("Bar_File_"+str(get_number(input_file_name)) + ".png")
plt.show()


plt.hist(plotdata[1], 20)
plt.title("Chi^2 of the various files")
plt.ylabel("Number of galaxies")
plt.xlabel('Chi^2 of the comparison')
plt.savefig("Hist_File_"+str(get_number(input_file_name)) + ".png")
plt.show()


print("Best few")
for i in range(4):
    print(str(get_number(result[i][1])) + " -> " + str(result[i][0])+"\n")
    
print("Worse few")
for i in range(4):
    print(str(get_number(result[-(1+i)][1])) + " -> " + str(result[-(i+1)][0])+"\n")

