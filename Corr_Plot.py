import sys
import matplotlib.pyplot as plt
import numpy as np

input_file_name = sys.argv[1]

properties = ['logmstar', 'dellogmstar', 'logage', 'dellogage', 'logtau', 'dellogtau', 'metal', 'delmetal']

data = {}
data['num'] = []
for p in properties:
    data[p] = []

#
#LOAD DATA
#

input_file = open(input_file_name, "r")
for line in input_file:
    values = line.split(' ')
    data['num'].append(int(values[0]))
    for i in range(len(properties)):
        data[ properties[i] ].append(float(values[i+1]))

#
#Plot data
#

MAXBINS = 50
plt.figure(1, figsize=(13,6))
plt.subplot(121)
plt.hist2d(data['logmstar'], data['logage'],  bins=MAXBINS)
plt.xlabel(r'logmstar')
plt.ylabel(r'logage')


plt.subplot(122)
plt.hist2d(data['logmstar'], data['logage'], range=[[9,12],[9.4,9.9]],  bins=MAXBINS)
plt.xlabel(r'logmstar')
plt.ylabel(r'logage')
plt.savefig("lms_la.png")
plt.show()


plt.figure(2, figsize=(13,6))
plt.subplot(121)
plt.hist2d(data['logmstar'], data['metal'], bins=MAXBINS)
plt.xlabel(r'logmstar')
plt.ylabel(r'metal')

plt.subplot(122)
plt.hist2d(data['logmstar'], data['metal'], range=[[9,11], [0,0.025]], bins=MAXBINS)
plt.xlabel(r'logmstar')
plt.ylabel(r'metal')
plt.savefig("lms_mt.png")
plt.show()


plt.figure(3, figsize=(13,6))
plt.subplot(121)
plt.hist2d(data['logmstar'], data['logtau'], bins=MAXBINS)
plt.xlabel(r'logmstar')
plt.ylabel(r'logtau')

plt.subplot(122)
plt.hist2d(data['logmstar'], data['logtau'], range=[[8,11],[8.5,9.9]], bins=MAXBINS)
plt.xlabel(r'logmstar')
plt.ylabel(r'logtau')
plt.savefig("lms_lt.png")
plt.show()


plt.figure(4, figsize=(13,6))
plt.subplot(121)
plt.hist2d(data['logage'], data['metal'], bins=MAXBINS)
plt.xlabel(r'logage')
plt.ylabel(r'metal')

plt.subplot(122)
plt.hist2d(data['logage'], data['metal'],range=[[9.5,9.9], [0,0.025]], bins=MAXBINS)
plt.xlabel(r'logage')
plt.ylabel(r'metal')
plt.savefig("la_mt.png")
plt.show()


plt.figure(5, figsize=(13,6))
plt.subplot(121)
plt.hist2d(data['logage'], data['logtau'], bins=MAXBINS)
plt.xlabel(r'logage')
plt.ylabel(r'logtau')

plt.subplot(122)
plt.hist2d(data['logage'], data['logtau'], range=[[9.5,9.9], [8.5, 9.9]], bins=MAXBINS)
plt.xlabel(r'logage')
plt.ylabel(r'logtau')
plt.savefig("la_lt.png")
plt.show()


plt.figure(6, figsize=(13,6))
plt.subplot(121)
plt.hist2d(data['metal'], data['logtau'], bins=MAXBINS)
plt.xlabel(r'metal')
plt.ylabel(r'logtau')

plt.subplot(122)
plt.hist2d(data['metal'], data['logtau'], range=[[0, 0.025], [8.5, 9.9] ], bins=MAXBINS)
plt.xlabel(r'metal')
plt.ylabel(r'logtau')
plt.savefig("mt_lt.png")
plt.show()


