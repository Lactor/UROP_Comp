import sys

input_file_name = sys.argv[1]
input_file = open(input_file_name, 'r')
output_file_name = sys.argv[2]
shift_factor = float(sys.argv[3])

FILE_SECOND_COLUMN = 4 #Position of the value when the line is split

data = [[], []] #first array wavelengths second intensities

for line in input_file:
    values = line.split(' ')
    print(values)
    data[0].append( float(values[0]))
    #print("Main WL Added: " +str(data[0][-1]) )

    data[1].append(float(values[ FILE_SECOND_COLUMN]))
          #Data in logspace

for i in range(len(data[0])-1):
    data[0][i] = data[0][i] + shift_factor*(data[0][i+1]-data[0][i])

output_file = open(output_file_name, 'w')
for i in range(len(data[0])-1):
    output_file.write(str(data[0][i]) + "  \t  " + str(data[1][i])+"  \n")


