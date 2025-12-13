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
# Binning data
#
nbin=50
bin_lim = np.linspace(0, 1, nbin+1)
bins=np.zeros(nbin)
for i in range(0, len(bin_lim)-1):
	bins[i]=0.5*(bin_lim[i]+bin_lim[i+1]) 
#
time = data1[:,0]
digitized = np.digitize(time, bin_lim)
mean1 = [fl1[digitized == i].mean() for i in range(1, len(bin_lim))]
stddev1 = [fl1[digitized == i].std() for i in range(1, len(bin_lim))]
#
time = data3[:,0]
digitized = np.digitize(time, bin_lim)
mean3 = [fl3[digitized == i].mean() for i in range(1, len(bin_lim))]
stddev3= [fl3[digitized == i].std() for i in range(1, len(bin_lim))]
#
# Escfrevendo saida em arquivos
#
f1 = open('ztfj0850_g.olc', 'w')
f2 = open('ztfj0850_r.olc', 'w')
for i in range(0, len(bin_lim)-1):
	f1.write("%.4f %.8f %.8f 0.0 1.0 0.0 1.0 0.0 1.0 \n" % (bins[i],mean1[i],stddev1[i],))
	f2.write("%.4f %.8f %.8f 0.0 1.0 0.0 1.0 0.0 1.0 \n" % (bins[i],mean3[i],stddev3[i],))
f1.close
f2.close
#print(bins)
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
ax.errorbar(bins,mean1,yerr=stddev1,fmt='ko',markersize=2,label='g band')
ax.errorbar(bins+1,mean1,yerr=stddev1,fmt='ko',markersize=2)
ax.errorbar(bins,mean3,yerr=stddev3,fmt='ro',markersize=2,label='r band')
ax.errorbar(bins+1,mean3,yerr=stddev3,fmt='ro',markersize=2)
#ax.errorbar(bins+1.0,bin_means,fmt='ko',markersize=2)
# ax.errorbar(data3[:,0],fl3,fmt='ro',markersize=2,label='r band')
# ax.errorbar(data3[:,0]+1.0,fl3,fmt='ro',markersize=2)
#ax[1].errorbar(data4[:,0],data4[:,1], yerr=data4[:,2],fmt='ro',markersize=3,label='50 bins')
ax.set_xlabel('Spin phase')
ax.set_ylabel('Flux (Jy)')
ax.set_title('ZTF J0850+0443')
#ax.invert_yaxis()
ax.legend()
plt.show()






