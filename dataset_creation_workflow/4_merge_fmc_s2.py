import numpy as np
import pandas as pd

df_fmc = pd.read_csv('modis_fmc_selection.csv', parse_dates=['time'])
df_fmc.rename({"id": "uid"}, axis='columns', inplace=True)
df_fmc = df_fmc.set_index(['time', 'uid'])

df_s2 = pd.read_csv('s2_reflectances.csv', parse_dates=['time'])

df_int = pd.DataFrame(columns=['time', 'uid', 'nbart_blue', 'nbart_green', 'nbart_red', 'nbart_nir_1', 'nbart_nir_2', 'nbart_swir_2', 'nbart_swir_3'])
    
for uid in df_s2.uid.unique():
    dfi = df_s2[df_s2['uid']==uid]
    dfi = dfi.set_index('time')

    dfi = dfi.resample('D').mean().interpolate()
    dfi['uid'] = uid
    dfi['time'] = dfi.index
    
    df_int = df_int.append(dfi)

df_int = df_int.set_index(['time', 'uid'])

df = pd.concat([df_int, df_fmc], axis=1).dropna()

df.to_csv("fmc_s2_reflectances.csv", index_label=['time', 'uid'], float_format='%.4f')

"""
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

ax = plt.axes(projection=ccrs.PlateCarree())
plt.title('Australia')
#plt.figure(figsize=(12,12))

ax.set_extent([112, 154, -44, -5.6], ccrs.PlateCarree())
ax.coastlines(resolution='110m')
for _, row in df[df.veg_type==2][['latitude','longitude']].iterrows():
    plt.plot(row['longitude'], row['latitude'],  markersize=5, marker='o', color='blue')

plt.show()
"""
