import pyfits
import math
import numpy as np
import sys
import glob
import os
import matplotlib.pyplot as plt


input_folder= sys.argv[1]
if input_folder[-1] != '/':
    input_folder += '/'

output_folder = sys.argv[2]
if output_folder[-1] != '/':
    output_folder += '/'

if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

data_files = glob.glob(input_folder+ "*.fit")

for file_name in data_files:
    print(file_name)
    fit_file = pyfits.open(file_name)

    print(np.shape(fit_file[0].data))
    if ('row1' in fit_file[0].header) and (fit_file[0].header['row1'] == 'Spectrum'):
        data_field = 1 - 1
                
    elif ('array1' in  fit_file[0].header) and (fit_file[0].header['array1'] == 'SPECTRUM'):
        data_field = 1 - 1

    if ('row2' in fit_file[0].header) and (fit_file[0].header['row2'] == 'Error'):
        error_field = 2 -1
                
    elif ('array3' in  fit_file[0].header) and (fit_file[0].header['array3'] == 'ERROR'):
        error_field = 3 - 1
        

    redshift = fit_file[0].header['z']

    x = np.linspace(float(fit_file[0].header['wmin']), float(fit_file[0].header['wmax']),np.shape(fit_file[0].data)[1] ) 
        #Creates the values of the wavelengths (NOT ENTIRELY SURE ABOUT VALIDITY OF THIS)
    
    data = [x, [],[]]

    for i in range(len(data[0])):
        data[0][i] *= 0.1**(10) # Turn from Angstrom to meters

        fl_wl = fit_file[0].data[data_field][i]*(0.1**7) #erg/(s.cm^2.m) (10^(-17 (from units) + 10 (from A to m))
        fl_fr = fl_wl * data[0][i]**2 / (3e8) #erg/(s.cm^2.Hz)
        data[1].append(fl_fr * 10**29) # to microjanskys
    
        #Same procedure as before
        err_fl_wl = fit_file[0].data[error_field][i]*(0.1**7)
        err_fl_fq = err_fl_wl *  data[0][i]**2 / (3e8)
        data[2].append(err_fl_fq*10**29)


    output = open(output_folder + "gama_"+ str(fit_file[0].header['cataid']) + ".txt", "w")
    output.write("%.8e\n"%(redshift))
    for i in range(len(data[0])):
        if data[1][i] == data[1][i] and data[1][i] >0:
            output.write("%.8e %.8e %.8e\n"%( data[0][i], data[1][i], data[2][i]))
    output.close()
