#
# Plot light curve and phase diagram
#
import matplotlib.pyplot as plt
import numpy as np
from astropy.timeseries import LombScargle
from scipy import stats
import statistics
import sys
#
# from scipy.stats import distributions
# import similaritymeasures
#
#
###########################################
#   Reading X-ray phase diagram
#
data1 = np.loadtxt('12lspeg_fot.txt',skiprows=0)
data2 = np.loadtxt('12lspeg_pol.txt.bias',skiprows=0)
#
time = data1[:,0]
mag  = data1[:,1]
#
time_pol = data2[:,0]
circ_pol = data2[:,1]
#########################################################
# convert magnitude to flux
flux = 10**(-0.4*(mag-12))
circ_pol = circ_pol* 0.01
#print(flux)
#print(len(mag))
#print(len(flux))
#print(len(circ_pol))
#########################################################
# criterio
delta_time = np.diff(time)
#print(time)
#print(delta_time)
moda = statistics.mode(delta_time)
#print(moda)
criterio = (moda*8*1.1)/2
#print(criterio)
#####   avarage  #####
#print(time)
#condicao = False
flux_pol = circ_pol*0.0
flux_ave = circ_pol*0.0
#
for i,x in enumerate(time_pol):
    print(i,x)
    indice = []
    print(x-criterio,x+criterio)
    for j,y in enumerate(time):
           # print(j)
           #for f,z in enumerate(flux):
           if (y > (x-criterio)) and (y < (x+criterio)):
                  indice.append(j)
           #avefluxo.append(np.average(z))
    print(indice)
    # print(flux[indice])
    flux_ave[i]=np.average(flux[indice])
flux_pol=circ_pol*flux_ave
#print(avefluxo,circ_pol[i],flux_pol[i])
#sys.exit("Sai!")
#########################################################
# Plot
plt.close('all')
#
#f, ax = plt.subplots(2, sharex=True)
f, ax = plt.subplots(5, sharex=True)
f.subplots_adjust(hspace=0.0)
#f.align_ylabels(ax[0:1])
#
ax[0].plot(time,flux,'b.',markersize=4)
ax[0].set_ylabel('Flux')
# ax[0].set_xlim(52455.2,52455.4)
#
ax[1].plot(time_pol,circ_pol,'b.',markersize=4)
ax[1].set_ylabel('Pol.')
#
ax[2].plot(time_pol,flux_ave,'b.',markersize=4)
ax[2].set_ylabel('Flux av.')
#
ax[3].plot(time_pol,flux_pol,'b.',markersize=4)
ax[3].set_ylabel('Pol.flux')
#
ax[4].plot(time,flux,'b.',markersize=4)
ax[4].plot(time_pol,flux_ave,'r.',markersize=4)
ax[4].set_ylabel('teste')
ax[4].set_xlabel('HJD')
#
plt.show()






