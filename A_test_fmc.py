import xarray as xr
import pandas as pd
import time
from datetime import datetime
import argparse
import os.path
from glob import glob
from pyproj import Proj, transform
import math

fmc_root = "/g/data/ub8/au/FMC/c6/"
tile_extent = 1111950.51966667
tile_size = 2400
sinu_proj = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs "
wgs84_proj = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs "

inProj = Proj(wgs84_proj)
outProj = Proj(sinu_proj)

def xy2tile(x, y):
    return int(math.floor(x/tile_extent)) + 18, -1*int(math.ceil(y/tile_extent)) + 9

def xy2ij(x, y):
    return int(2400*(x % tile_extent) / tile_extent),  int(2400 - (2400 * (y % tile_extent) / tile_extent))

df = pd.read_csv('modis_fmc_selection.csv')  

for _, row in df.iterrows():
    d = datetime.strptime(row['time'], "%Y-%m-%d")
    x, y = transform(inProj,outProj, row['longitude'], row['latitude'])
    
    h, v = xy2tile(x, y)
    i, j = xy2ij(x, y)

    with xr.open_dataset(fmc_root + f"fmc_c6_{d.year}_h{h:02d}v{v:02d}.nc") as ds:
        print(row['fmc_mean'], ds["lfmc_mean"].isel(x=i, y=j).sel(time=d).values)

