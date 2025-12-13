#
# Plot light curve and phase diagram
#
import matplotlib.pyplot as plt
import numpy as np
from astropy.timeseries import LombScargle
# from scipy import stats
# from scipy.stats import distributions
# import similaritymeasures
#
#
###########################################
#   Reading X-ray phase diagram
#
# data1 = np.loadtxt('bocet_fot_p1_orb.txt',skiprows=0)
data1 = np.loadtxt('6bocet_fot.txt',skiprows=0)
#
t1=data1[:,0]
mag1=data1[:,1]
# mag1_error=data1[:,2]
#
# Removendo a media dos dados
#
mag_mean1=np.mean(mag1)
mag_c1=mag1-mag_mean1
#mag_c1=mag1
#
data1 = np.loadtxt('11bocet_fot.txt',skiprows=0)
#
t2=data1[:,0]
mag2=data1[:,1]
#
# Removendo a media dos dados
#
mag_mean2=np.mean(mag2)
mag_c2=mag2-mag_mean2
# mag_c2=mag2
#
#
data1 = np.loadtxt('12bocet_fot.txt',skiprows=0)
#
t3=data1[:,0]
mag3=data1[:,1]
#
# Removendo a media dos dados
#
mag_mean3=np.mean(mag3)
mag_c3=mag3-mag_mean3
# mag_c3=mag3
#
#
data1 = np.loadtxt('19bocet_fot.txt',skiprows=0)
#
t4=data1[:,0]
mag4=data1[:,1]
#
# Removendo a media dos dados
#
mag_mean4=np.mean(mag4)
mag_c4=mag4-mag_mean4
# mag_c4=mag4
#
# time=np.concatenate((t1,t2,t3))
# mag_c=np.concatenate((mag_c1,mag_c2,mag_c3))
# mag_error=np.concatenate((mag1_error,mag2_error,mag3_error))
time=np.concatenate((t1,t2,t3,t4))
mag_c=np.concatenate((mag_c1,mag_c2,mag_c3,mag_c4))
# mag_error=np.concatenate((mag1_error,mag2_error,mag3_error,mag4_error))
# time=1.*t1
# mag_c=1.*mag_c1
# mag_error=1.*mag1_error
#
#  Filter data
#
filter="no"
#filter="yes"
#
##### Lomb Scargle
#
# limites em minutos
p1=6.
p2=13.
# 
p1=p1/60./24.0
p2=p2/60./24.0
# 
# limites em dias
# p1=0.
# p2=1.
#
#
# Numero de frequencias
#
n_freq=1e6
frequency = np.linspace(1./p2, 1./p1, n_freq)
#
#
#  Fazendo o Lomb-Scargle
#
ls = LombScargle(time, mag_c)
# ls = LombScargle(time, mag_c,mag_error)
power = ls.power(frequency)
probabilities = [0.001]
fap=ls.false_alarm_level(probabilities) 
#
best_frequency = frequency[np.argmax(power)]
best_period=1./best_frequency
#
# best_period=50.9/60/24
# best_frequency=1./best_period
#
print(' ')
print('Best period in days  ', best_period)
print('Best period in hours  ', best_period*24.)
print('Best period in minutes  ', best_period*24.*60.)
print('False alarm probability of 0.001  ',fap)
print(' ')
#
# Calculando phase diagram
#
to=2456746.57311
phase=((time-to)%best_period)/best_period
#
# Binning data in the best period
#
number_bins=6
center_bin=np.zeros(number_bins)
bin_means=np.zeros(number_bins)
bin_size=1./number_bins
bins = np.linspace(0, 1, number_bins+1)
digitized = np.digitize(phase, bins)
# print(bins)
# print(digitized)
for i in range(1, len(bins)):
    im=i-1
    center_bin[im]=bins[i]-0.5*bin_size
    bin_means[im]=np.mean(mag_c[digitized == i])
#    print(i,center_bin[im],bin_means[im]) 
#
#    Model sinuosoidal
# 
y_fit = ls.model(time, best_frequency)
#
# Filtrando
#
if (filter != "no"):
	f= open("bocet_fot_p1_orb_p2_509.txt","x")
	mag_filtered=np.zeros(len(mag_c))
	for i in range(0, len(mag_c)):
#
#    Aqui eu filtro por media do bin - nao eh bom
#
# 		mag_filtered[i]=mag[i]-bin_means[digitized[i]-1]
#  
#    Aqui filtro por Model sinuosoidal
# 
		mag_filtered[i]=mag_c[i]-y_fit[i]
		f.write(f"{time[i]} {mag_c[i]} {mag_filtered[i]} \n")
	
#
	f.close()
#
#### Plot
#
plt.close('all')
#
f, ax = plt.subplots(4, sharex=False)
f.subplots_adjust(hspace=0.4)
#f.align_ylabels(ax[0:1])
#
ax[0].plot(time,mag_c,'b.',markersize=4)
ax[0].plot(time,y_fit,'g-',markersize=4)
ax[0].set_xlabel('HJD')
# ax[0].set_xlim(52455.2,52455.4)
#
ax[1].plot(1./frequency*24.*60.,power)
ax[1].set_xlabel('Period (minute)')
xmin=p1*24.*60.
xmax=p2*24.*60.
# ax[1].plot(1./frequency,power)
# ax[1].set_xlabel('Period (d)')
# xmin=p1
# xmax=p2
ax[1].hlines(fap,xmin,xmax,linestyles='dashed')
#
ax[2].plot(frequency,power)
ax[2].set_xlabel('Frequency (1/d)')
xmin=1./p1
xmax=1./p2
# ax[2].plot(1./frequency,power)
# ax[2].set_xlabel('Period (d)')
# xmin=p1
# xmax=p2
ax[2].hlines(fap,xmin,xmax,linestyles='dashed')
#
ax[3].plot(phase,mag_c,'b.',markersize=4)
ax[3].plot(phase+1.0,mag_c,'b.',markersize=4)
ax[3].plot(phase,y_fit,'g.',markersize=4)
ax[3].plot(phase+1.0,y_fit,'g.',markersize=4)
ax[3].plot(center_bin,bin_means,'r-',markersize=4)
ax[3].plot(center_bin+1.0,bin_means,'r-',markersize=4)
ax[3].set_xlabel('Phase')
# ax[3].set_xlim(0,2)
#ax[3].plot(t_fit,y_fit,'k-')
#
#
# print(time.size)
# print(time_b.size)
# print(time_v.size)
plt.show()





