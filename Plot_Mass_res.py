
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

data_file_name = sys.argv[1]
results_folder = sys.argv[2]

if results_folder[-1] != '/':
    results_folder += '/'

data_extracted = {'num': []  }

tem_red = []
tem_ms = []
tem_mf = []

data_file = open(data_file_name, "r")
for line in  data_file:
    values = line.split(' ')
    data_extracted['num'] = int(values[0])
    tem_red.append( float(values[1]))
    tem_ms.append(float(values[2]))
    tem_mf.append(float(values[3]))

data_extracted['red'] = np.array(tem_red)
data_extracted['ms'] = np.array(tem_ms)
data_extracted['mf'] = np.array(tem_mf)

avg_error = np.sum(data_extracted['ms']-data_extracted['mf'])/len(data_extracted['ms'])
std_error = np.sqrt( np.sum((data_extracted['ms']-data_extracted['mf'] - avg_error)**2)/len(data_extracted['ms']))

print("AVG error: ", avg_error)
print("STD error: ", std_error)

avg_relerror = np.sum(data_extracted['ms']/data_extracted['mf'])/len(data_extracted['ms'])
std_relerror = np.sqrt( np.sum((data_extracted['ms']/data_extracted['mf'] - avg_error)**2)/len(data_extracted['ms']))

print("AVG relerror: ",avg_relerror )
print("STD error: ", std_relerror)


#PLOT ms as a function of mf
plt.plot(data_extracted['mf'], data_extracted['ms'], "bo")
plt.plot([0,100],[0,100], "r-")
plt.xlabel("Mass Fast")
plt.ylabel("Mass Sim")
plt.axis( [np.min(data_extracted['mf']), np.max(data_extracted['ms']), np.min(data_extracted['ms']), np.max(data_extracted['ms'])])
plt.title("Plot of the mass of the simulation as a function of the mass of fast")
plt.savefig(results_folder + "mf_ms.png")
plt.show()


#PLOT difference in mass as a function of redshift


plt.plot(data_extracted['red'], data_extracted['ms'] - data_extracted['mf'], "bo")
plt.plot([0,100],[0,0], "r-")
plt.xlabel("Redshift")
plt.ylabel("Diference M_sim - M_data")
plt.title("Plot of the difference in masses as a function of redshift")
plt.axis( [ np.min(data_extracted['red']), np.max(data_extracted['red']),np.min(data_extracted['ms'] - data_extracted['mf']), np.max(data_extracted['ms'] - data_extracted['mf'])])
plt.savefig(results_folder + "red_dif.png")
plt.show()

# Plot ratio of masses as a function of redshift

plt.plot(data_extracted['red'], data_extracted['ms']/data_extracted['mf'], "bo")
plt.plot([0,100],[1,1], "r-")
plt.xlabel("Redshift")
plt.ylabel(" M_sim/M_data")
plt.title("Plot of the ratio in masses as a function of redshift")
plt.axis( [ np.min(data_extracted['red']), np.max(data_extracted['red']), np.min(data_extracted['ms']/data_extracted['mf']), np.max(data_extracted['ms']/data_extracted['mf'])])
plt.savefig(results_folder + "red_rat.png")
plt.show()

# Plot ratio of masses as a function of redshift

plt.plot(data_extracted['red'], data_extracted['ms']/data_extracted['mf'], "bo")
plt.plot([0,100],[1,1], "r-")
plt.xlabel("Redshift")
plt.ylabel(" M_sim/M_data")
plt.title("Plot of the ratio in masses as a function of redshift")
plt.axis( [ np.min(data_extracted['red']), np.max(data_extracted['red']),0.7,1.5])
plt.savefig(results_folder + "red_ratwin.png")
plt.show()

# Plot log of ratio of masses as a function of redshift

plt.plot(data_extracted['red'], np.log10(data_extracted['ms']/data_extracted['mf']), "bo")
plt.plot([0,100],[0,0], "r-")
plt.xlabel("Redshift")
plt.ylabel("Log(M_sim/M_data)")
plt.title("Plot of the log of ratio of masses as a function of redshift")
plt.axis( [np.min(data_extracted['red']), np.max(data_extracted['red']), np.min(np.log10(data_extracted['ms']/data_extracted['mf'])), np.max(np.log10(data_extracted['ms']/data_extracted['mf']))])
plt.savefig(results_folder + "red_lograt.png")
plt.show()



