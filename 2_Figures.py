import sys
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator, LogLocator)
import xarray as xr

######################################################### Initialisation ###########################################################################################################################################################################

CC_300K   = 2.4373e6 / (461.52 * 300.**2.)

ds= xr.open_dataset('/chemin/vers/lequel/enregristrer/le/datataset.nc')

B1_precip_per  = np.log(ds.sel(sst_bins=slice(300,302.5)).precip_per).polyfit(dim='sst_bins',deg=1).isel(degree=0).polyfit_coefficients           # Beta 1 de l'équation (1) de la méthode de Hatsukal et al. (2020)
B1_precip_mean = np.log(ds.sel(sst_bins=slice(300,302.5)).precip_mean).polyfit(dim='sst_bins',deg=1).isel(degree=0).polyfit_coefficients

pente_precip_per  = (np.exp(B1_precip_per ) - 1.) * 100.
pente_precip_mean = (np.exp(B1_precip_mean) - 1.) * 100.

contrib = 100.* ds.precip_volume / ds.precip_volume.sum('SST')

###############################################################################################################################################################################################################################################################
###############################################################################################################################################################################################################################################################
#################################### Création des plots #######################################################################################################################################################################################################
###############################################################################################################################################################################################################################################################
###############################################################################################################################################################################################################################################################

#Contribution au cumul 

fig,ax = plt.subplots(figsize=(14,13))

ax.set_title('1DD 30S-30N 2007-2017 T(t-48h)',fontsize=20)
ax.set_xlabel('SST(t-48h) daily average [K]', fontsize=20)
ax.set_ylabel('Contribution to total rainfall amount [%]', fontsize=20)
ax.axvline(x=300.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
ax.axvline(x=302.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
ax.fill_between(ds.sst_bins, contrib-contrib, contrib+contrib,alpha=0.04, facecolor='k',linewidth=0)
ax.plot(ds.sst_bins,contrib,label='Label', color='k', linewidth=5, linestyle='-')
ax.set_xlim([299.25, 303.75])	
ax.set_ylim([0,20])
ax.set_xticks(np.arange(300, 304, step=1))
ax.set_yticks(np.arange(0, 25, step=5))
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.yaxis.set_minor_locator(MultipleLocator(1))
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.tick_params(direction='in',which='major',labelsize=20,length=15,color='k')
ax.tick_params(direction='in',which='minor',length=5,color='k')
ax.legend(fontsize=14)

plt.savefig('/chemin/vers/plot.png', dpi=300)


# ###############################################################################################################################################################################################################################################################

# #Nombre de gridbox

fig, axs = plt.subplots(1,2,figsize=(22,10), facecolor='w', edgecolor='k',sharey=False)
# fig.suptitle('',fontsize=25)
axs[0].set_title('1DD 30S-30N Ocean 99.9th percentile 2012-2020 T(t-48h) CC 6.0%.$\mathregular{K^{-1}}$',fontsize=14)
axs[1].set_title('1DD 30S-30N Ocean 99.99th percentile 2012-2020 T(t-48h) CC 6.0%.$\mathregular{K^{-1}}$',fontsize=14)

axs[0].plot(ds.sst_bins,ds.isel(percentile=12).n_grid_ext, label='Label', color='k', linewidth=5)
axs[1].plot(ds.sst_bins,ds.isel(percentile=16).n_grid_ext, label='Label', color='b', linewidth=5)

for i in range(0,2):
	axs[i].set_yscale('log')
	axs[i].set_ylim([10**0,10**3])
	# axs[i].set_yticks(np.arange(10**0,10**4, step=10**1))
	# axs[i].yaxis.set_minor_locator(MultipleLocator(1))
	axs[i].set_ylabel('# extreme gridboxess', fontsize=17)
	axs[i].set_xlabel('SST(t-48h) daily average [K]', fontsize=17)
	axs[i].axvline(x=300.25, color='k', linestyle='--',linewidth=2,dashes=[4,4])
	axs[i].axvline(x=302.25, color='k', linestyle='--',linewidth=2,dashes=[4,4])
	axs[i].set_xlim([299.25, 303.75])	
	axs[i].set_xticks(np.arange(300, 304, step=1))
	axs[i].xaxis.set_minor_locator(MultipleLocator(0.5))
	# axs[i].get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
	axs[i].tick_params(direction='in',which='major',labelsize=15,length=15,color='k')
	axs[i].tick_params(direction='in',which='minor',length=5,color='k')
	axs[i].legend(loc=4,fontsize=8)

plt.savefig('/chemin/vers/plot.png', dpi=300)

################################################################################################################################################################################################################################################################

#moyenne de la précip extrême dans les 10% de la valeur du centile

fig, ax = plt.subplots(figsize=(9,10), facecolor='w', edgecolor='k',sharey=False)
ax.set_yscale('log')
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
for icc in np.arange(-2,5,0.16):
 	ax.plot(ds.sst_bins,np.exp( CC_300K * (ds.sst_bins-ds.sst_bins[0]) + icc),dashes=[4, 6, 14, 6],color='lightgrey',linewidth=2)
ax.set_title('2007-2017',fontsize=19)
ax.plot(ds.sst_bins,ds.isel(quantile=12).precip_mean, color='k', linewidth=5, linestyle='-')				
ax.set_ylim([101,271])
ax.set_yticks(np.arange(110,280, step=20))
ax.yaxis.set_minor_locator(MultipleLocator(5))
ax.set_ylabel('Precipitation [mm.$\mathregular{day^{-1}}$]', fontsize=17)
ax.set_xlabel('SST(t-48h) daily average [K]', fontsize=17)
ax.axvline(x=300.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
ax.axvline(x=302.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
ax.set_xlim([299.25, 303.75])	
ax.set_xticks(np.arange(300, 304, step=1))
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
# ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.tick_params(direction='in',which='major',labelsize=15,length=15,color='k')
ax.tick_params(direction='in',which='minor',length=5,color='k')
# lines   = ax.get_lines()
# legend1 = ax.legend([lines[i] for i in [53,54,55]], tempshort, loc=3, fontsize = 14)
# legend2 = ax.legend([lines[i] for i in [44,47,50,53,56,59,62]], vrai_nom[ens], loc=4, fontsize = 14)
# ax.add_artist(legend1)
# ax.add_artist(legend2)
# ax.legend(loc=2,fontsize=8)
fig.tight_layout(w_pad=5,h_pad=3,rect=[0, 0.03, 1, 0.95])

plt.savefig('/chemin/vers/plot.png', dpi=300)