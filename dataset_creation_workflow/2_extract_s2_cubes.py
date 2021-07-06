import datacube
from datacube.drivers.netcdf import write_dataset_to_netcdf
import xarray as xr
import pandas as pd
import time
import argparse
import os.path

parser = argparse.ArgumentParser(description='select veg type for processor')
parser.add_argument('--veg_type', type=int, help='an integer for the accumulator')

args = parser.parse_args()

dc = datacube.Datacube(app="loading_data")

measurements= ["nbart_blue", "nbart_green", "nbart_red","nbart_nir_1", "nbart_nir_2", "nbart_swir_2", "nbart_swir_3"] 
    
df = pd.read_csv('modis_fmc_selection.csv')  
df = df.set_index(['latitude', 'longitude', 'id'])

for lat, lon, uid in df.index.unique():
    if os.path.isfile(f"/g/data/xc0/user/pablo/{uid}.nc"):
        continue

    if int(uid[0])!=args.veg_type:
        continue

    print(uid)
    start = time.time()
    ds_a = dc.load(product="s2a_ard_granule", x=(lon-0.001, lon+0.001), y=(lat+0.001, lat-0.001), time=("2015-01","2019-01"), measurements=measurements, output_crs="EPSG:3577", resolution=(-10, 10), group_by="solar_day")
    ds_b = dc.load(product="s2b_ard_granule", x=(lon-0.001, lon+0.001), y=(lat+0.001, lat-0.001), time=("2015-01","2019-01"), measurements=measurements, output_crs="EPSG:3577", resolution=(-10, 10), group_by="solar_day")

    ds = xr.concat([ds_a, ds_b], dim='time').sortby('time')
    write_dataset_to_netcdf(ds, f"/g/data/xc0/user/pablo/{uid}.nc")
    print(time.time()-start)
