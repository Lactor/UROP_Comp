#!/bin/bash

sim_sed_folder=/n/ghernquist/ptorrey/Machado/code/UROP_Comp/100_100/Formated
sim_gal_property_file=/n/ghernquist/ptorrey/Machado/code/UROP_Comp/trim_aux_properties.txt
results_dir=/n/ghernquist/ptorrey/Machado/results
gama_input_files=/n/ghernquist/ptorrey/Machado/code/UROP_Comp/100_100/Gama/gama_*txt

mpirun -np 8 python Bay_MPI.py ${sim_sed_folder}  ${sim_gal_property_file} ${results_dir} ${gama_input_files}



