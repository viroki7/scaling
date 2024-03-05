import glob
import numpy as np
import xarray as xr
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

"""
Ce script lit des données de température, de précipitation ainsi qu'un masque terre/mer
afin de calculer les centiles de précipitations dans des bins de température
sur les océans, ainsi que d'autres statistiques. Il enregistre ensuite le 
dataset en sortie.

Auteur:
Victorien De Meyer (de_meyer.victorien@uqam.ca), UQAM-ESCER

Crée le:
3 Mars 2024
""""

#Ouverture du fichier NetCDF du masque terre/mer
ds_landseamask = xr.open_dataset('/chemin/vers/le/masque_terre_mer.nc')
#Dans le cas où le fichier a une variable 'time', pour s'en affranchir (car inutile dans notre cas), décommenter si nécessaire la ligne suivante
#ds_landseamask = ds_landseamask.isel(time=0) 

#Liste des fichiers NetCDF de température
filenames_sst = glob.glob('/chemin/vers/les/données/de/SST.nc') #exemple : glob.glob('/home/USER/DATA/NCDF/SST/*/SST_*.nc')
#Ouverture des fichiers de température
ds_temp = xr.open_mfdataset(filenames_sst)
#Sélection des latitudes tropicales uniquement
ds_temp_tropics = ds_temp.sel(latitude=slice(30,-30))
#Lag de la température de 2 pas de temps (i.e. 2 jours si le jeu de données est journalier)
temp_shift = ds_temp_tropics['sst_variable'].shift(time=2) #remplacer 'sst_variable' par le nom de la variable dans le NetCDF

#Liste des fichiers NetCDF de précipitation
filenames_rain = glob.glob('/chemin/vers/les/données/de/girafe.nc') #exemple : glob.glob('/home/USER/DATA/NCDF/RAIN/*/RAIN_*.nc')
#Ouverture des fichiers de précipitation
ds_rain = xr.open_mfdataset(filenames_rain)
#Sélection des latitudes tropicales uniquement
ds_rain_tropics = ds_rain.sel(latitude=slice(30,-30))

  
### Calcul des statistiques de précipitation dans chaque bin de température ###

#choix des bins de température, ici des bins de 0.5K entre 285K et 314.5K
bins = np.arange(285,315,0.5)

#Label des bins, qui correspond ici au milieu de chaque bin (ex : 285.25 pour le bin [285,285.5])
bin_label = np.arange(285.25,314.75,0.5)

#Chacun des centiles à calculer
per = [100.-10^2.,100.-10^1.75,100.-10^1.5,100.-10^1.25,100.-10^1.,100.-10^0.75,
       100.-10^0.5,100.-10^0.25,100.-10^0,100.-10^(-0.25),100.-10^(-0.5),
       100.-10^(-0.75),100.-10^(-1.),100.-10^(-1.25),100.-10^(-1.5),100.-10^(-1.75),100.-10^(-2.)]

#Déchunk de la coordonnée "time" du dataset afin de calculer les centiles sans générer d'erreur
rain_tropics = ds_rain_tropics['precipitation_variable'].chunk(dict(time=-1)) #remplacer 'precipitation_variable' par le nom de la variable dans le NetCDF

#Regroupement des précipitations supérieures à 1mm/j et sur les océans en bin de température
rain_tropics_binned = rain_tropics.where((rain_tropics >= 1.) & (ds_landseamask['masque_variable'] == 0.)).groupby_bins(temp_shift, bins=bins, labels=bin_label) #remplacer 'masque_variable' par le nom de la variable dans le NetCDF

#Calcul des centiles conditionnés (>1mm/j) dans chaque bin de température sur les zones océaniques uniquement (masque = 0)
rain_tropics_centile = rain_tropics_binned.quantile(per, method='lower')

#Calcul du volume des pluies (>1mm/j) dans chaque bin de température sur les zones océaniques uniquement (masque = 0)
rain_tropics_volume  = rain_tropics_binned.sum()


#A présent les mêmes calculs sont faits, mais plutôt que de calculer les statistiques pour les précipitations
#supérieures à la valeur du centile, elles sont calculées sur les précipitations dans un certain intervalle (en %)
#autour de la valeur du centile

moyennes_dataarray = []
count_dataarray = []
intervalle = 0.1 #Correspond à l'intervalle, en %, que l'on prend autour du centile. Ici, 0.1 pour 10%

for label, group in tqdm(rain_tropics_binned): #Pour chacun des bins de température
    moyennes = []
    count = []

    for i, quantile in enumerate(per): #Pour chacun des centiles

        donnees_dans_intervalle = group.where(abs(group - rain_tropics_centile.sel(sst_bins=label, quantile=quantile)) < intervalle * rain_tropics_centile.sel(sst_bins=label, quantile=quantile)) #Toutes les données de précipitations dans l'intervalle
        moyennes.append(donnees_dans_intervalle.mean()) #La moyenne du taux de précipitation dans l'intervalle du centile
        count.append(donnees_dans_intervalle.count()) #Le nombre de donnée de taux de précipitation dans l'intervalle du centile

    moyennes_dataarray.append(xr.DataArray(moyennes, dims=('quantile',), coords={'quantile': per, 'sst_bins': label})) #Création du DataArray avec la dimention centile
    count_dataarray.append(xr.DataArray(count, dims=('quantile',), coords={'quantile': per, 'sst_bins': label}))

moyennes_par_bin = xr.concat(moyennes_dataarray, dim='sst_bins').sortby('sst_bins') #Concaténation des DataArray de la moyenne pour en avoir un unique avec la dimension sst_bins
count_par_bin    = xr.concat(count_dataarray, dim='sst_bins').sortby('sst_bins')


#On merge les 4 DataArrays contenant les statistiques calculées en un seul Dataset
ds = xr.merge([rain_tropics_centile.rename('precip_per'), rain_tropics_volume.rename('precip_volume'), moyennes_par_bin.rename('precip_mean'), count_par_bin.rename('n_grid_ext')])

#Enregristrement du Dataset en NetCDF
ds.to_netcdf('/chemin/vers/lequel/enregristrer/le/datataset.nc')
