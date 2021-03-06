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
mcd43_root = "/g/data/u39/public/data/modis/lpdaac-tiles-c6/MCD43A4.006"
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

d = datetime(2018, 12, 3)
lat = -34.5
lon = 143.1

x, y = transform(inProj,outProj, lon, lat)
h, v = xy2tile(x, y)
i, j = xy2ij(x, y)

with xr.open_dataset(fmc_root + f"fmc_c6_{d.year}_h{h:02d}v{v:02d}.nc") as ds:
    print(ds["lfmc_mean"].isel(x=i, y=j).sel(time=d).values)

modis_glob = f"{mcd43_root}/{d.strftime('%Y.%m.%d')}/MCD43A4.A{d.year}{d.timetuple().tm_yday:03d}.h{h:02d}v{v:02d}.006.*.hdf"
modis_tiles = glob(modis_glob)
if len(modis_tiles) != 1:
    exit()

with xr.open_dataset(modis_tiles[0]) as ds:
    for i in [1,2,4,6,7]:
        print(i, ds[f"Nadir_Reflectance_Band{i}"].isel({'XDim:MOD_Grid_BRDF':i, 'YDim:MOD_Grid_BRDF':j}).values)


