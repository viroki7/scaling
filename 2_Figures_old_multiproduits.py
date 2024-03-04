#-*- coding:UTF-8 -*-

######################################################### Bibliothèque ###########################################################################################################################################################################

import sys
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator, LogLocator)
import xarray as xr

plt.clf()
plt.close('all')

######################################################### Initialisation ###########################################################################################################################################################################

prodshort = np.array(['GSMArtg','CMORg','TMPA','IMFC', 'HOAP','GPCPnew','GPCPun','MSWE','TAPR','PERS'])
vrai_nom  = np.array(['GSMaP','CMORPH','TMPA','IMERG','HOAPS','GPCP','GPCPv1.3','MSWEP','TAPEER','PERSIANN'])
color     = ['#FF0000','#00FF00','#FFA500','#7F7F7F','#ED3AFF','#FDFF64','#CECECE','#003AFF','#008708','#74B1FF']
ens       = np.array([0,1,2,3,4,5,7])
tempshort = np.array(['OSTIA','OISST','RSS'])
tempshort = np.array(['OISST','RSS'])
# #Sans HOAPS
# ens=np.array([0,1,2,3,5])
nprod     = len(prodshort[ens])
nsst      = len(tempshort)
nbint     = 60.
deltabint = 0.5
baset     = 285.
xtemp     = np.arange(nbint) * deltabint + baset + deltabint / 2
xper      = [100.-10**2.,100.-10**1.75,100.-10**1.5,100.-10**1.25,100.-10**1.,100.-10**0.75,100.-10**0.5,100.-10**0.25,100.-10**0,100.-10**(-0.25),100.-10**(-0.5),100.-10**(-0.75),100.-10**(-1.),100.-10**(-1.25),100.-10**(-1.5),100.-10**(-1.75),100.-10**(-2.)]
nprod     = len(prodshort[ens])
nsst      = len(tempshort)
nper      = len(xper)
CC_300K   = 2.4373e6 / (461.52 * 300.**2.)


ds_brut = xr.open_mfdataset([f'/home/vdemeyer/SCALING/DATA/NCDF/Scaling_{iprodsst}(t-48h)_2001-2017_1DD_10%.nc' for iprodsst in tempshort], concat_dim = 'sst_prod', combine = 'nested')
ds      = ds_brut.assign_coords(SST = xtemp, sst_prod = tempshort, precip_prod = prodshort, quantile = xper)

B1_precip_per  = np.log(ds.sel(SST=slice(300,302.5)).precip_per).polyfit(dim='SST',deg=1).isel(degree=0).polyfit_coefficients           # Beta 1 de l'équation (1) de la méthode de Hatsukal et al. (2020)
B1_precip_mean = np.log(ds.sel(SST=slice(300,302.5)).precip_mean).polyfit(dim='SST',deg=1).isel(degree=0).polyfit_coefficients

pente_precip_per  = (np.exp(B1_precip_per ) - 1.) * 100.
pente_precip_mean = (np.exp(B1_precip_mean) - 1.) * 100.

contrib = 100.* ds.precip_volume / ds.precip_volume.sum('SST')
# contrib.sel(SST=slice(300,302.5)).isel(precip_prod=ens).sum('SST').mean('precip_prod').values
###############################################################################################################################################################################################################################################################
###############################################################################################################################################################################################################################################################
#################################### Création des plots #######################################################################################################################################################################################################
###############################################################################################################################################################################################################################################################
###############################################################################################################################################################################################################################################################

#Contribution au cumul 

# fig,ax = plt.subplots(figsize=(14,13))

# ax.set_title('1DD 30S-30N 2007-2017 T(t-48h)',fontsize=20)
# ax.set_xlabel('SST(t-48h) daily average [K]', fontsize=20)
# ax.set_ylabel('Contribution to total rainfall amount [%]', fontsize=20)
# ax.axvline(x=300.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
# ax.axvline(x=302.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
# ax.fill_between(ds.SST, contrib.isel(sst_prod=0).mean(dim='precip_prod')-contrib.isel(sst_prod=0).std(dim='precip_prod'), contrib.isel(sst_prod=0).mean(dim='precip_prod')+contrib.isel(sst_prod=0).std(dim='precip_prod'),alpha=0.04, facecolor='k',linewidth=0)
# ax.plot(ds.SST,contrib.isel(sst_prod=0).mean(dim='precip_prod'),label='OSTIA product mean', color='k', linewidth=5, linestyle='-')
# ax.fill_between(ds.SST, contrib.isel(sst_prod=1).mean(dim='precip_prod')-contrib.isel(sst_prod=1).std(dim='precip_prod'), contrib.isel(sst_prod=1).mean(dim='precip_prod')+contrib.isel(sst_prod=1).std(dim='precip_prod'),alpha=0.04, facecolor='k',linewidth=0)
# ax.plot(ds.SST,contrib.isel(sst_prod=1).mean(dim='precip_prod'),label='OISST product mean', color='k', linewidth=5, linestyle='--')
# ax.fill_between(ds.SST, contrib.isel(sst_prod=2).mean(dim='precip_prod')-contrib.isel(sst_prod=2).std(dim='precip_prod'), contrib.isel(sst_prod=2).mean(dim='precip_prod')+contrib.isel(sst_prod=2).std(dim='precip_prod'),alpha=0.04, facecolor='k',linewidth=0)
# ax.plot(ds.SST,contrib.isel(sst_prod=2).mean(dim='precip_prod'),label='RSS product mean', color='k', linewidth=5, linestyle=':')
# ax.set_xlim([299.25, 303.75])	
# ax.set_ylim([0,20])
# ax.set_xticks(np.arange(300, 304, step=1))
# ax.set_yticks(np.arange(0, 25, step=5))
# ax.xaxis.set_minor_locator(MultipleLocator(0.5))
# ax.yaxis.set_minor_locator(MultipleLocator(1))
# ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
# ax.tick_params(direction='in',which='major',labelsize=20,length=15,color='k')
# ax.tick_params(direction='in',which='minor',length=5,color='k')
# ax.legend(fontsize=14)

# plt.savefig('/home/vdemeyer/SCALING/PLOT/contrib_2007-2017.png', dpi=300)



# fig,ax = plt.subplots(figsize=(14,13))

# ax.set_title('1DD 30S-30N 2007-2017 T(t-48h)',fontsize=20)
# ax.set_xlabel('SST(t-48h) daily average [K]', fontsize=20)
# ax.set_ylabel('Contribution to total rainfall amount [%]', fontsize=20)
# ax.axvline(x=300.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
# ax.axvline(x=302.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
# ax.fill_between(ds.SST, contrib.isel(sst_prod=0).mean(dim='precip_prod')-contrib.isel(sst_prod=0).std(dim='precip_prod'), contrib.isel(sst_prod=0).mean(dim='precip_prod')+contrib.isel(sst_prod=0).std(dim='precip_prod'),alpha=0.04, facecolor='k',linewidth=0)
# ax.plot(ds.SST,contrib.isel(sst_prod=0).mean(dim='precip_prod'),label='OSTIA product mean', color='k', linewidth=5, linestyle='-')
# ax.fill_between(ds.SST, contrib.isel(sst_prod=1).mean(dim='precip_prod')-contrib.isel(sst_prod=1).std(dim='precip_prod'), contrib.isel(sst_prod=1).mean(dim='precip_prod')+contrib.isel(sst_prod=1).std(dim='precip_prod'),alpha=0.04, facecolor='k',linewidth=0)
# ax.plot(ds.SST,contrib.isel(sst_prod=1).mean(dim='precip_prod'),label='OISST product mean', color='k', linewidth=5, linestyle='--')
# ax.fill_between(ds.SST, contrib.isel(sst_prod=2).mean(dim='precip_prod')-contrib.isel(sst_prod=2).std(dim='precip_prod'), contrib.isel(sst_prod=2).mean(dim='precip_prod')+contrib.isel(sst_prod=2).std(dim='precip_prod'),alpha=0.04, facecolor='k',linewidth=0)
# ax.plot(ds.SST,contrib.isel(sst_prod=2).mean(dim='precip_prod'),label='RSS product mean', color='k', linewidth=5, linestyle=':')
# ax.set_xlim([289.25, 306.75])	
# ax.set_ylim([0,20])
# ax.set_xticks(np.arange(290, 307, step=1))
# ax.set_yticks(np.arange(0, 25, step=5))
# ax.xaxis.set_minor_locator(MultipleLocator(0.5))
# ax.yaxis.set_minor_locator(MultipleLocator(1))
# ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
# ax.tick_params(direction='in',which='major',labelsize=20,length=15,color='k')
# ax.tick_params(direction='in',which='minor',length=5,color='k')
# ax.legend(fontsize=14)

# plt.savefig('/home/vdemeyer/SCALING/PLOT/contrib_elargie_2007-2017.png', dpi=300)


# ###############################################################################################################################################################################################################################################################

# #Nombre de gridbox

# fig, axs = plt.subplots(1,2,figsize=(22,10), facecolor='w', edgecolor='k',sharey=False)
# # fig.suptitle('',fontsize=25)
# axs[0].set_title('1DD 30S-30N Ocean 99.9th percentile 2012-2020 T(t-48h) CC 6.0%.$\mathregular{K^{-1}}$',fontsize=14)
# axs[1].set_title('1DD 30S-30N Ocean 99.99th percentile 2012-2020 T(t-48h) CC 6.0%.$\mathregular{K^{-1}}$',fontsize=14)
# for iprod in range(0,nprod):
# 	axs[0].plot(ds.SST,ds.isel(precip_prod=ens[iprod],percentile=12,sst_prod=isst).n_grid_ext,label=''+vrai_nom[ens[iprod]]+'', color=color[ens[iprod]], linewidth=5)
# 	axs[1].plot(ds.SST,ds.isel(precip_prod=ens[iprod],percentile=16,sst_prod=isst).n_grid_ext,label=''+vrai_nom[ens[iprod]]+'', color=color[ens[iprod]], linewidth=5)
# for i in range(0,2):
# 	axs[i].set_yscale('log')
# 	axs[i].set_ylim([10**0,10**3])
# 	# axs[i].set_yticks(np.arange(10**0,10**4, step=10**1))
# 	# axs[i].yaxis.set_minor_locator(MultipleLocator(1))
# 	axs[i].set_ylabel('# extreme gridboxess', fontsize=17)
# 	axs[i].set_xlabel(''+tempshort[isst]+' SST(t-48h) daily average [K]', fontsize=17)
# 	axs[i].axvline(x=300.25, color='k', linestyle='--',linewidth=2,dashes=[4,4])
# 	axs[i].axvline(x=302.25, color='k', linestyle='--',linewidth=2,dashes=[4,4])
# 	axs[i].set_xlim([299.25, 303.75])	
# 	axs[i].set_xticks(np.arange(300, 304, step=1))
# 	axs[i].xaxis.set_minor_locator(MultipleLocator(0.5))
# 	# axs[i].get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# 	axs[i].tick_params(direction='in',which='major',labelsize=15,length=15,color='k')
# 	axs[i].tick_params(direction='in',which='minor',length=5,color='k')
# 	axs[i].legend(loc=4,fontsize=8)


################################################################################################################################################################################################################################################################

#percentile

# fig, ax = plt.subplots(figsize=(9,10), facecolor='w', edgecolor='k',sharey=False)
# ax.set_yscale('log')
# ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
# for icc in np.arange(-2,5,0.16):
#  	ax.plot(ds.SST,np.exp( CC_300K * (ds.SST-ds.SST[0]) + icc),dashes=[4, 6, 14, 6],color='lightgrey',linewidth=2)
# ax.set_title('2007-2017',fontsize=19)
# for iprod in range(0,nprod):
# 	ax.plot(ds.SST,ds.isel(sst_prod=0,precip_prod=ens[iprod],quantile=12).precip_mean, color=color[ens[iprod]], linewidth=5, linestyle='-')	
# 	ax.plot(ds.SST,ds.isel(sst_prod=1,precip_prod=ens[iprod],quantile=12).precip_mean, color=color[ens[iprod]], linewidth=5, linestyle='--')
# 	ax.plot(ds.SST,ds.isel(sst_prod=2,precip_prod=ens[iprod],quantile=12).precip_mean, color=color[ens[iprod]], linewidth=5, linestyle=':')					
# ax.set_ylim([101,271])
# ax.set_yticks(np.arange(110,280, step=20))
# ax.yaxis.set_minor_locator(MultipleLocator(5))
# ax.set_ylabel('Precipitation [mm.$\mathregular{day^{-1}}$]', fontsize=17)
# ax.set_xlabel('SST(t-48h) daily average [K]', fontsize=17)
# ax.axvline(x=300.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
# ax.axvline(x=302.25, color='k', alpha=0.65, linestyle='-',linewidth=2)#,dashes=[4,4])
# ax.set_xlim([299.25, 303.75])	
# ax.set_xticks(np.arange(300, 304, step=1))
# ax.xaxis.set_minor_locator(MultipleLocator(0.5))
# # ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# ax.tick_params(direction='in',which='major',labelsize=15,length=15,color='k')
# ax.tick_params(direction='in',which='minor',length=5,color='k')
# lines   = ax.get_lines()
# legend1 = ax.legend([lines[i] for i in [53,54,55]], tempshort, loc=3, fontsize = 14)
# legend2 = ax.legend([lines[i] for i in [44,47,50,53,56,59,62]], vrai_nom[ens], loc=4, fontsize = 14)
# ax.add_artist(legend1)
# # ax.add_artist(legend2)
# # ax.legend(loc=2,fontsize=8)
# fig.tight_layout(w_pad=5,h_pad=3,rect=[0, 0.03, 1, 0.95])

# plt.savefig('/home/vdemeyer/SCALING/PLOT/scaling_2007-2017.png', dpi=300)



pente_precip_mean_prodmean = pente_precip_mean.sel(precip_prod = prodshort[ens]).mean(dim = 'precip_prod')
pente_precip_mean_prodstd  = pente_precip_mean.sel(precip_prod = prodshort[ens]).std(dim = 'precip_prod')

fig,ax = plt.subplots(figsize=(7.5, 7.5))
ax.set_title('2001-2017 ; SST(t-48h) ; [300 K; 302.5 K]', fontsize = 13)
ax.fill_between(100. - np.array(xper), pente_precip_mean_prodmean.sel(sst_prod = 'OSTIA') - pente_precip_mean_prodstd.sel(sst_prod = 'OSTIA'), pente_precip_mean_prodmean.sel(sst_prod = 'OSTIA') + pente_precip_mean_prodstd.sel(sst_prod = 'OSTIA'), facecolor = 'b', alpha = 0.09)
# ax.fill_between(100. - np.array(xper), pente_precip_mean_prodmean.sel(sst_prod = 'OISST') - pente_precip_mean_prodstd.sel(sst_prod = 'OISST'), pente_precip_mean_prodmean.sel(sst_prod = 'OISST') + pente_precip_mean_prodstd.sel(sst_prod = 'OISST'), facecolor = 'r', alpha = 0.09)
ax.fill_between(100. - np.array(xper), pente_precip_mean_prodmean.sel(sst_prod = 'RSS')   - pente_precip_mean_prodstd.sel(sst_prod = 'RSS'), pente_precip_mean_prodmean.sel(sst_prod = 'RSS')     + pente_precip_mean_prodstd.sel(sst_prod = 'RSS'),   facecolor = 'g', alpha = 0.09)
ax.plot(100. - np.array(xper), pente_precip_mean_prodmean.sel(sst_prod = 'OSTIA'), linewidth = 3, linestyle = '-',  c = 'b', label = 'OSTIA')
# ax.plot(100. - np.array(xper), pente_precip_mean_prodmean.sel(sst_prod = 'OISST'), linewidth = 3, linestyle = '--', c = 'r', label = 'OISST')
ax.plot(100. - np.array(xper), pente_precip_mean_prodmean.sel(sst_prod = 'RSS'),   linewidth = 3, linestyle = ':',  c = 'g', label = 'RSS  ')
ax.set_xlabel('Percentile', fontsize=15)
ax.set_ylabel('Scaling rate [%.$K^{-1}$]', fontsize=15)
ax.set_xscale('log')
ax.set_yticks(np.arange(-50, 50, step=2))
ax.yaxis.set_minor_locator(MultipleLocator(1))
ax.set_ylim([0,15])
ax.axhline(y=(np.exp( CC_300K * 2.)-1)*50., color='k',linewidth=1.5,alpha=1)
ax.text(0.95,(np.exp( CC_300K * 2.)-1)*50.+0.02,'CC', horizontalalignment='left', color='k',fontsize=20,alpha=1)
# ax.set_xlim([1e1,1e-2])
# ax.set_xticklabels(['useless','$\mathregular{99.99^{ème}}$','$\mathregular{99.9^{ème}}$','$\mathregular{99^{ème}}$','$\mathregular{90^{ème}}$'])
ax.set_xlim([10**0,1e-2])
ax.set_xticklabels(['useless','$\mathregular{99.99^{th}}$','$\mathregular{99.9^{th}}$','$\mathregular{99^{th}}$'])
ax.xaxis.set_minor_locator(LogLocator(base=10,subs=[10**1.75,10**1.5,10**1.25]))
ax.tick_params(top=True,right=True,which='major',direction='in',labelsize=15,length=9,color='k',pad=7)
ax.tick_params(top=True,right=True,which='minor',direction='in',length=3,color='k')
ax.legend(fontsize=15)

plt.savefig('/home/vdemeyer/SCALING/PLOT/scaling_percentile_10%_2001-2017.png', dpi = 300)

#################################################### Écriture des plots #######################################################################################################################################################################################

# # pdf = matplotlib.backends.backend_pdf.PdfPages('/home/vdemeyer/MCS/PLOT/plot_ocean_2012-2020_5%_(t-48h).pdf')
# pdf = matplotlib.backends.backend_pdf.PdfPages('/home/vdemeyer/SCALING/PLOT/plot_ocean_2012-2020_5%_(t-48h).pdf')
# for fig1 in range(1, plt.gcf().number+1):
# 	# pdf.savefig(fig1,bbox_inches='tight')
# 	pdf.savefig(fig1)
# pdf.close()
# plt.clf()
# plt.close('all')	
# print('pdf file written!')