import xarray as xr
import pandas as pd

samples = pd.read_csv('modis_fmc_selection.csv')  
samples = samples.set_index(['latitude', 'longitude', 'id'])

df = pd.DataFrame(columns=['time', 'uid', 'nbart_blue', 'nbart_green', 'nbart_red', 'nbart_nir_1', 'nbart_nir_2', 'nbart_swir_2', 'nbart_swir_3'])
df = df.set_index(['time', 'uid'])

for lat, lon, uid in samples.index.unique():
    print(uid)
    ds = xr.open_dataset(f"/g/data/xc0/user/pablo/{uid}.nc")

    ds = ds.mean(dim=["x","y"])
    dfi = ds.to_dataframe()
    dfi.drop('spatial_ref', axis=1, inplace=True)
    dfi['time'] = dfi.index
    dfi['uid'] = uid
    dfi = dfi.set_index(['time', 'uid'])
    df = df.append(dfi)

df.to_csv("s2_reflectances.csv", index_label=['time', 'uid'], float_format='%.4f')
