#!/usr/bin/env python
# coding: utf-8

# In[24]:


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import xarray
import cartopy.crs as ccrs
from scipy.signal import detrend
#import eofs


# In[25]:


pfad = "/home/srvx11/lehre/users/a1127897/ipython/Klima2/Data/mslp_daily/"


# In[26]:


def open_df(pfad):
    df = xr.open_mfdataset(pfad+'*.nc',chunks={'initial_time0_hours':504,'g0_lat_1':29,'g0_lon_2':29})
    df = df.rename({'initial_time0_hours':'time','g0_lat_1':'lat','g0_lon_2':'lon','PRMSL_GDS0_MSL':'mslp'}).drop("initial_time0_encoded")
    df.coords['lon'] = (df.coords['lon'] + 180) % 360 - 180
    return df
def mean_std(df):
    df_mean = df.resample(time='1D').mean().chunk({'time':504,'lat':29,'lon':29})
    df_roll_mean = df_mean.rolling(time=20,center=True).mean().dropna('time').groupby('time.dayofyear').mean(axis=0)
    
    new_dim = df_mean.rolling(time=20, center=True).construct('dim_roll_days') #Die +- 10 Tage in eine eigene Dim stecken
    stacked_dim =new_dim.stack(line=('lat','lon')) # Stack into Dimension lat, lon
    df_std = stacked_dim.groupby('time.dayofyear').std() #Std der 20 Tage pro Tag des Jahres berechnen
    return df_mean,df_std
def anomaly_nor(df,mean,std):
    anomaly = df - mean
    anomaly_norm = anomaly / std
    return anomaly,anomaly_norm


# In[30]:


df = open_df(pfad)
df_mean,df_std = mean_std(df)
df_ano, df_norm_ano = anomaly_nor(df,df_mean,df_std)


# In[31]:


df_norm_ano


# In[ ]:




