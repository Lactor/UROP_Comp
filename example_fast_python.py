import sunpy.sunpy__load
import sunpy.broadband_filters
import glob
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.ticker import MultipleLocator
import cosmocalc
import readsubfHDF5
import tables
import hdf5lib
import math

from scipy import ndimage
from scipy.optimize import curve_fit
from scipy import stats



def write_fast_sdss_input_file(target_dir, redshift, filename='sunrise_sdss.cat'):

    dist = (cosmocalc.cosmocalc(redshift, H0=70.4, WM=0.2726, WV=0.7274))['DL_Mpc']
    dist *= 1e6

    sunrise_band_index_list = [2, 3, 4, 5, 6, 18, 20]                               ### this filter index list must match the one below
    fast_filter_number      = [156, 157, 158, 159, 160, 162, 163 ]                     ### right now need to do this by hand based on:
                                                                            ### fast_filter_ref = "~/FAST/FAST_v1.0/Filters/FILTER.RES.v7.R300.info.txt"

    #===============================================================#
    #                       write header                            #
    #===============================================================#
    f = open(filename,'w')
    f.write("#  id  ")
    for filter_nr in fast_filter_number:
        f.write("F"+str(filter_nr)+"  E"+str(filter_nr)+"  ")

    f.write("z_spec")
    f.write("\n")

    #===============================================================#
    #                       write body                              #
    #===============================================================#
    subfolder_list = glob.glob(target_dir+"sub*")
    for subdir in subfolder_list[0:]:
        print subdir
        filelist=glob.glob(subdir+"/broad*fits")
        filelist.sort()

        for file in filelist[0:]:
            print file
            tag = file[file.index('band_')+5:file.index('.fits')]
            f.write(str(tag))

            fluxes = sunpy.sunpy__fast.load_all_microjansky_fluxes(file,dist=dist)
            for band in sunrise_band_index_list:
                f.write("  "+str(fluxes[band])+"  "+str(fluxes[band]*0.1))
            f.write("  "+str(redshift)+"  \n")

    #===============================================================#
    #                       close                                   #
    #===============================================================#
    f.close()
    #===============================================================#

def load_all_microjansky_fluxes(filename,camera=0,dist=5e8):
    ab0 = 23.93
    apparent_magnitudes = load_all_broadband_apparent_magnitudes(filename,camera=camera,dist=dist)
    flux = 10.0**(-1.0/2.5 * (apparent_magnitudes - ab0))
    return flux


def load_all_broadband_apparent_magnitudes(filename,camera=0,dist=4e8):
    dist_modulus = 5.0 * ( np.log10(dist) - 1.0 )
    apparent_magnitudes = dist_modulus + load_all_broadband_photometry(filename,camera=camera)
    return apparent_magnitudes


def load_all_broadband_photometry(filename,camera=0):
    if (not os.path.exists(filename)):
        print "file not found:", filename
        return 0

    hdulist = fits.open(filename)
    data = hdulist['FILTERS'].data['AB_mag_nonscatter0']
    return data


