; PROGRAMME PRINCIPALE DES PARAMETRES DES MCS SUR OCEAN, PENSER A LA Tb DANS LA LECTURE

; si besoin des fichiers des fichiers load_*, me contacter à de_meyer.victorien@uqam.ca

nn                      = 360
mm                      = 180
mmtrop                  = 60
nmcs                    = 25
lon                     = findgen(nn) - 179.5
latitude                = 89.5 - indgen(mm)
lat                     = findgen(mmtrop) - 29.5
indtrop                 = where(latitude ge -30 AND latitude le 30, clat)
wetday_threshold        = 1.0
str_wetday_threshold    = string(wetday_threshold,format='(f3.1)')
per                     = [100.-10^2.,100.-10^1.75,100.-10^1.5,100.-10^1.25,100.-10^1.,100.-10^0.75,100.-10^0.5,100.-10^0.25,100.-10^0,100.-10^(-0.25),100.-10^(-0.5),100.-10^(-0.75),100.-10^(-1.),100.-10^(-1.25),100.-10^(-1.5),100.-10^(-1.75),100.-10^(-2.)]
nper                    = n_elements(per)
ystart                  = 2001
yend                    = 2017
nday                    = JULDAY(12,31,yend)-JULDAY(1,1,ystart) + 1
nbint                   = 60.
deltabint               = 0.5
baset                   = 285.
xtemp                   = findgen(nbint) * deltabint + baset + deltabint / 2
prodshort               = ['GSMArtg','CMORg','TMPA','IMFC', 'HOAP','GPCPnew','GPCPun','MSWE','TAPR','PERS']
tempshort               = ['OSTIA']
; tempshort               = ['OISST']
; tempshort               = ['RSS']
nprod                   = n_elements(prodshort)
nsst                    = n_elements(tempshort)
perce_precip            = fltarr(nprod,nsst,nbint,nper)
precip_volume           = fltarr(nprod,nsst,nbint)
mean_precip             = fltarr(nprod,nsst,nbint,nper)
n_grid_ext              = fltarr(nprod,nsst,nbint,nper)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

lsmtnday = fltarr(nn,mm,nday)
load_lsmt_1DD_global_etopo, lsmt

for i = 0, nday-1 do lsmtnday(*,*,i) = lsmt

lsmtnday_tropics_lag = lsmtnday(*,indtrop,2:nday-1) 

for isst=0,nsst-1 do begin
;#################### LOAD TEMPERATURE ###################

	temp_nday_tropics=fltarr(nn,mmtrop,nday)

	print, '#############################################'
	print, ''
	print, tempshort(isst)

	k = 0
	for iyear = ystart, yend do begin
	    nday_year=JULDAY(12,31,iyear)-JULDAY(1,1,iyear)+1
		if tempshort(isst) eq 'OSTIA' then begin
		load_OSTIA_season, iyear, data_t
		temp_nday_tropics(*,*,k:k+nday_year-1) = data_t
	endif
	if tempshort(isst) eq 'OISST' then begin
		load_OISST_V1_season, iyear, data_t
		temp_nday_tropics(*,*,k:k+nday_year-1) = data_t
	endif
	if tempshort(isst) eq 'RSS' then begin
		load_RSS_season, iyear, data_t
		temp_nday_tropics(*,*,k:k+nday_year-1) = data_t
	endif
	    k = k + nday_year
	endfor;iyear

	ind_T_nan = where_xyz(finite(temp_nday_tropics) eq 0, c_T_nan, xind = x_T_nan, yind = y_T_nan, zind = z_T_nan)

	temp_nday_tropics_lag = temp_nday_tropics(*,*,0:nday-3)

	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

	for iprod=0,nprod-1 do begin
	;#################### LOAD PRECIP ###################


		print, ''
		print, '## ',prodshort(iprod),' ##'

		rainfall_nday = fltarr(nn,mm,nday)

		k = 0
		for iyear = ystart,yend do begin
		    nday_year = JULDAY(12,31,iyear)-JULDAY(1,1,iyear)+1
		    if prodshort(iprod) eq 'TMPA' and iyear eq 2020 then begin 
		    	rainfall_nday(*,*,k:k+nday_year-1) = !VALUES.F_NAN
			endif else if prodshort(iprod) eq 'TMPA' and iyear eq 2019 then begin 
				load_gridded_1DD_global, prodshort(iprod), iyear, data
				rainfall_nday(*,*,k:k+nday_year-2) = data
				rainfall_nday(*,*,k+nday_year-1)   = !VALUES.F_NAN
			endif else if prodshort(iprod) eq 'TAPR' and iyear lt 2012 then begin
				rainfall_nday(*,*,k:k+nday_year-1) = !VALUES.F_NAN
			endif else if prodshort(iprod) eq 'TAPR' and iyear eq 2017 then begin
				nday_year_amputed = JULDAY(12,14,iyear)-JULDAY(1,1,iyear)+1
				load_gridded_1DD_global, prodshort(iprod), iyear, data
				rainfall_nday(*,*,k:k+nday_year_amputed-1) = data
				rainfall_nday(*,*,k+nday_year_amputed:k+nday_year-1) = !VALUES.F_NAN	
			endif else if prodshort(iprod) eq 'MSWE' and iyear ge 2017 then begin
				rainfall_nday(*,*,k:k+nday_year-1) = !VALUES.F_NAN  
			endif else if prodshort(iprod) eq 'MSWE' and iyear eq 2017 then begin
				nday_year_amputed = JULDAY(10,31,iyear)-JULDAY(1,1,iyear)+1
				load_gridded_1DD_global, prodshort(iprod), iyear, data
				rainfall_nday(*,*,k:k+nday_year_amputed-1) = data
				rainfall_nday(*,*,k+nday_year_amputed:k+nday_year-1) = !VALUES.F_NAN
			endif else begin
				load_gridded_1DD_global,prodshort(iprod), iyear, data
				rainfall_nday(*,*,k:k+nday_year-1) = data
			endelse
		    k = k + nday_year
		endfor;iyear

		rainfall_nday_tropics=rainfall_nday(*,indtrop,*)

		rainfall_nday_tropics_lag = rainfall_nday_tropics(*,*,2:nday-1)

		;#####################################################################################################################################################################################################################################################################################################################################
		;#####################################################################################################################################################################################################################################################################################################################################

		;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; calcul du percentile pour chaque T   

		for itbin = 0, nbint - 1 do begin

		   	lowt = baset + itbin * deltabint
		  	higt = baset + (itbin + 1) * deltabint       	

			ind = where(temp_nday_tropics_lag ge lowt AND temp_nday_tropics_lag lt higt AND lsmtnday_tropics_lag eq 0. AND finite(rainfall_nday_tropics_lag) eq 1 and rainfall_nday_tropics_lag gt wetday_threshold, ct)

			if ct gt 1 then begin
				perce_precip(iprod,isst,itbin,*) = percentile(rainfall_nday_tropics_lag(ind), per)
				precip_volume(iprod,isst,itbin) = total(rainfall_nday_tropics_lag(ind), /NAN)
			endif else begin
				goto, norain
			endelse

		;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; recherche des indices où la pluie est 10% autour de per et calcul des stat	

			for iper = 0, nper - 1 do begin	

				ind_ext = where_xyz(temp_nday_tropics_lag ge lowt AND temp_nday_tropics_lag lt higt AND lsmtnday_tropics_lag eq 0. AND finite(rainfall_nday_tropics_lag) eq 1 AND ABS(rainfall_nday_tropics_lag-perce_precip(iprod,isst,itbin,iper)) lt .1  * perce_precip(iprod,isst,itbin,iper), cext, xind = xext, yind = yext, zind = zext)
				
				mean_precip(iprod,isst,itbin,iper)          = MEAN(rainfall_nday_tropics_lag(xext,yext,zext), /nan)
			  	n_grid_ext(iprod,isst,itbin,iper)           = cext

			endfor;iper
			norain:
		endfor ;tbin
	endfor ;iprod
endfor ;isst
;#####################################################################################################################################################################################################################################################################################################################################
;#####################################################################################################################################################################################################################################################################################################################################		

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; écriture des fichiers

id = NCDF_CREATE('/home/vdemeyer/SCALING/DATA/NCDF/Scaling_'+tempshort+'(t-48h)_2001-2017_1DD_10%.nc', /CLOBBER, /NETCDF4_FORMAT)
NCDF_CONTROL, id, /FILL

sstid        = NCDF_DIMDEF(id, 'SST', nbint)
prodsstid    = NCDF_DIMDEF(id, 'sst_prod', nsst)
prodprecipid = NCDF_DIMDEF(id, 'precip_prod', nprod)
perid        = NCDF_DIMDEF(id, 'quantile', nper)

id_precip_volume      = NCDF_VARDEF(id, 'precip_volume', [prodprecipid, prodsstid, sstid], /FLOAT) ;100.*precip_volume(itbin)/TOTAL(precip_volume)
id_perce_precip       = NCDF_VARDEF(id, 'precip_per', [prodprecipid, prodsstid, sstid,perid], /FLOAT)
id_mean_precip        = NCDF_VARDEF(id, 'precip_mean', [prodprecipid, prodsstid, sstid,perid], /FLOAT)
id_n_grid_ext         = NCDF_VARDEF(id, 'ngrid_ext', [prodprecipid, prodsstid, sstid,perid], /FLOAT)

NCDF_ATTPUT, id, id_precip_volume, 'long_name', 'Rainfall volume'
NCDF_ATTPUT, id, id_precip_volume, 'units', 'mm'
NCDF_ATTPUT, id, id_perce_precip, 'long_name', 'Precipitation quantile value'
NCDF_ATTPUT, id, id_perce_precip, 'units', 'mm/day'
NCDF_ATTPUT, id, id_mean_precip, 'long_name', 'Average precipitation'
NCDF_ATTPUT, id, id_mean_precip, 'units', 'mm/day'
NCDF_ATTPUT, id, id_n_grid_ext, 'long_name', 'Number of extreme grid boxes'

NCDF_CONTROL, id, /ENDEF

NCDF_VARPUT, id, id_precip_volume, precip_volume   
NCDF_VARPUT, id, id_perce_precip, perce_precip       
NCDF_VARPUT, id, id_mean_precip, mean_precip
NCDF_VARPUT, id, id_n_grid_ext, n_grid_ext

NCDF_CLOSE, id


print,'NCDF written'
print,''

end

