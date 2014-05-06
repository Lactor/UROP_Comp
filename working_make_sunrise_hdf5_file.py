import glob
import os
import sys
import sunpy.sunpy__load
import numpy as np
from mpi4py import MPI
import readsubfHDF5
import tables
import hdf5lib
import time
import astropy.io.fits as fits

proceed_efficiently=1

#=========================================================#
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n_tasks = size
this_task = rank
#=========================================================#
#=========================================================#
base="/n/ghernquist/Illustris/Runs/Illustris-1"
file="/n/ghernquist/Illustris/Runs/Illustris-1/groups_135/fof_subhalo_tab_135.0.hdf5"
f=hdf5lib.OpenFile(file)
n_subhalos = hdf5lib.GetAttr(f, "Header", "Nsubgroups_Total")
f.close()

file="parsed_snapshots/snapshot_135/subfolder_000/broadband_1.fits"
band_names=sunpy.sunpy__load.load_broadband_effective_wavelengths(file)
n_bands = band_names.shape[0]

local_nodust_mag_array  = np.zeros((n_bands,n_subhalos))
global_nodust_mag_array = np.zeros((n_bands,n_subhalos))

local_dust_mag_array  = np.zeros((n_bands,n_subhalos))
global_dust_mag_array = np.zeros((n_bands,n_subhalos))

broadband_names=sunpy.sunpy__load.load_broadband_names(file)
#=========================================================#
#=========================================================#
conversion_factors = np.array([
           1414.9754,       3252.8839,      8861.3927,      15388.527,      26510.168,
           38857.102,       54997.022,      799727.87,      1361532.1,      534103.57,
           1.0,        9233.2672,      13679.932,      29766.960,      45087.541,
           21039.889,       100543.67,      174395.10,      174086.21,      311201.35,
           255220.65,       12726.292,      23796.477,      41020.953,      56976.495,
	   75133.397,       104062.80,      148513.29,      33210.013,      55712.553,
           90423.202,       149046.78,      254609.27,      450496.28,      810513.36,
           1292268.5])
conversion_factors *= 13.0
#=========================================================#
#=========================================================#

folderlist = glob.glob("parsed_snapshots/snap*135")
for folder in folderlist[0:5]:
    subfolderlist = glob.glob(folder+'/subfolder*')
    for subfolder in subfolderlist:
      subfolder_nr = int(subfolder[subfolder.index('folder_')+7:])
      
      if ((subfolder_nr % n_tasks) == this_task):
       print "processing subfolder "+subfolder+" on task"+str(this_task)

       broadbandlist = glob.glob(subfolder+'/broad*fits')
       for file in broadbandlist:
	  start_file = time.time()
          size = 239238720			### os.path.getsize(file)
          if this_task == 0:
	    print "    processing file "+file+" on task "+str(this_task)
          if size != 239238720:
              print "bad file: "+file
              os.remove(file)
          else:

	      start_read = time.time()
	      if proceed_efficiently==0:
                  photometry = sunpy.sunpy__load.load_all_broadband_photometry(file)
                  images     = sunpy.sunpy__load.load_all_broadband_images(file)
                  tau_maps   = sunpy.sunpy__load.load_all_tau_maps(file)
                  sd_factor  = sunpy.sunpy__load.load_surface_density_normalization_factor(file)
	      else:
                  hdulist = fits.open(file)
		  camera=0
#=========================================================================================#
                  photometry = np.array( hdulist['FILTERS'].data['AB_mag_nonscatter0'] )
#=========================================================================================#
                  camera_string = 'CAMERA'+str(camera)+'-BROADBAND-NONSCATTER'
                  images = np.array( hdulist[camera_string].data )
                  images[ images < 1e-20 ] = 1e-20
#=========================================================================================#
		  redshift = hdulist[1].header['REDSHIFT']
		  effective_wavelengths = np.array( hdulist['FILTERS'].data['lambda_eff'] )

		  camera_string = 'CAMERA'+str(camera)+'-AUX'
                  aux_image = np.array( hdulist[camera_string].data )
                  cold_gas_map       = aux_image[0,:,:]
		  cold_gas_metal_map = aux_image[1,:,:]

		  n_bands = effective_wavelengths.shape[0]
		  n_pixels = cold_gas_map.shape[0]

		  tau_maps = np.zeros((n_bands,n_pixels,n_pixels))

		  A_lambda_eff = (effective_wavelengths / (0.55 * 1e-6))**-0.7

		  index = cold_gas_map < 1e-10
		  cold_gas_map[index] = 1e-10
		  cold_gas_metal_map[index] = 1e-10 * 1e-2

		  s=1.35
		  b=-0.5
		  z_solar=0.02
		  nf= 4.28e-8
		  f_cover=0.33

		  band_index = 0
		  map = np.array( (1.0 + redshift)**b * ( ( cold_gas_metal_map/cold_gas_map) / z_solar)**s * cold_gas_map * nf )

		  for wavelength in effective_wavelengths:
		    tau_maps[band_index,:,:] = map*A_lambda_eff[band_index]             ##np.tile(1e-5,(512,512))
		    band_index += 1

		  index = tau_maps < 1e-5
		  tau_maps[index] = 1e-5
#=========================================================================================#
		  aux_image = hdulist[camera_string]
		  sd_factor = aux_image.header['CD1_1']
#=========================================================================================#
                  hdulist.close()


	      end_read   = time.time()
	      if this_task == 0:
	          print "  file read time is: "+str(end_read - start_read)
 		  sys.stdout.flush()
	
	      sd_factor2 = sd_factor**2
	      start_image_manip = time.time()
              for band_index in range(0,len(photometry)):
		  conversion_factor = conversion_factors[band_index]
		  lum_image      = images[band_index,:,:] * (conversion_factor * sd_factor2)
		  adj_lum_image  = np.multiply( lum_image ,  np.divide( (1.0 - np.exp(-1.0*tau_maps[band_index,:,:]) ) , (tau_maps[band_index,:,:])  ) )

		  index = int(file[file.index('band_')+5:file.index('.fits')])

#		  if n_tasks <= 1:
#                      print "sunrise pre-tabulated value: "+str(tabulated_value)
#                      print "image tabulated value:       "+str(-2.5 * np.log10( np.sum(     lum_image) ))
#                      print "dust image tabulated_value:  "+str(-2.5 * np.log10( np.sum( adj_lum_image)))
#                      print index
#                      print " "
#
		  local_nodust_mag_array[band_index,index] = -2.5 * np.log10( np.sum(     lum_image) )
		  local_dust_mag_array[  band_index,index] = -2.5 * np.log10( np.sum( adj_lum_image) )

	      end_image_manip = time.time()
	      if this_task == 0:
                    print "  image manipulation time is: "+str(end_image_manip - start_image_manip)

          end_file = time.time()
	  if this_task == 0:
	      print "total file time is: "+str(end_file - start_file)
	      print " "
	      sys.stdout.flush()

comm.Barrier()
comm.Allreduce(local_nodust_mag_array, global_nodust_mag_array, op=MPI.SUM)
comm.Allreduce(local_dust_mag_array,   global_dust_mag_array,   op=MPI.SUM)


if this_task == 0:
    print " "
    print " "
    print "... Begining writing no-dust HDF5 file on task "+str(this_task)+" ..."
    print " "
 
    f = tables.openFile("sunrise_nodust_catalog.hdf5", mode="w")
    band_index=0
    for band in broadband_names:
	print band
        band=band+'.'
        f.createArray(f.root, band[0:band.index('.')], global_nodust_mag_array[band_index,:])
	band_index+=1

    f.close()


if this_task == 1:
    print " "
    print " "
    print "... Begining writing dusty HDF5 file on task "+str(this_task)+" ..."
    print " "

    f = tables.openFile("sunrise_dust_catalog.hdf5", mode="w")
    band_index=0
    for band in broadband_names:
        print band
        band=band+'.'
        f.createArray(f.root, band[0:band.index('.')], global_dust_mag_array[band_index,:])
        band_index+=1

    f.close()








