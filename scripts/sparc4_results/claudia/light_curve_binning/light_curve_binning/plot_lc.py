#
# Rotina que plot espectro de entrada para o Cyclops
#
#
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
# from astropy.timeseries import LombScargle
# from scipy import stats
# from scipy.stats import distributions
# import similaritymeasures
#
# def func(x, a, b):
#     return a * np.exp(b / x) + 1.0
#
############################################
# 
# Creating the x range of the plot
#
# x=np.arange(3050,11000,10)
#
###########################################
#   Reading spectrum
#
data1= np.loadtxt('ZTFJ0850_CHIMERA_corrected_g.txt',skiprows=0)
data3= np.loadtxt('ZTFJ0850_CHIMERA_corrected_r.txt',skiprows=0)
#
fl1=3631*(10**(-0.4*data1[:,1])) # em Jy
fl3=3631*(10**(-0.4*data3[:,1])) # em Jy
#
#### Plot
#
plt.close('all')
#
f, ax = plt.subplots()
# f, ax = plt.subplots(2, sharex=True)
# f.subplots_adjust(hspace=0.0)
# f.align_ylabels(ax[0:1])
#
ax.errorbar(data1[:,0],fl1,fmt='ko',markersize=2,label='g band')
ax.errorbar(data1[:,0]+1.0,fl1,fmt='ko',markersize=2)
ax.errorbar(data3[:,0],fl3,fmt='ro',markersize=2,label='r band')
ax.errorbar(data3[:,0]+1.0,fl3,fmt='ro',markersize=2)
#ax[1].errorbar(data4[:,0],data4[:,1], yerr=data4[:,2],fmt='ro',markersize=3,label='50 bins')
ax.set_xlabel('Spin phase')
ax.set_ylabel('Flux (Jy)')
ax.set_title('ZTF J0850+0443')
#ax.invert_yaxis()
ax.legend()
plt.show()






