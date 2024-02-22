import xarray as xr                                                                                                               
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
import pandas as pd

ds = xr.open_mfdataset([f"/g/data/ub8/au/FMC/c6/mosaics/mask_{y}.nc" for y in range(2015,2019)]) # concatenate netcdf files into one datacube
#ds = ds.isel(longitude=slice(4000,4500), latitude=slice(4000,4500))

veg_map_mask = ds.quality_mask.where(ds.quality_mask == ds.quality_mask.isel(time=0)).all(dim='time') # pixel value == True if veg classification never changes across years
veg_map = ds.quality_mask.isel(time=0).where(veg_map_mask) # restrict veg mask to persistent veg type across years (with pixels values corresponding to veg id, PROBABLY quality_mask is actually a vegetation type mask) 
#print(np.sum(veg_map.values==1))
    
ds = xr.open_mfdataset([f"/g/data/ub8/au/FMC/c6/mosaics/fmc_c6_{y}.nc" for y in range(2015,2019)])
#ds = ds.isel(longitude=slice(4000,4500), latitude=slice(4000,4500))

obs_freq_mask = (ds.fmc_mean.notnull().sum(dim='time')/ds.time.shape[0])>0.9 # mask for selecting only pixels with not null values in at least the 90% of the time steps
veg_map = veg_map.where(obs_freq_mask) # restrict veg mask to those pixels whose FMC value is present in at least 90% of time steps
#print(np.sum(veg_map.values==1))

df = pd.DataFrame(columns=['time', 'latitude', 'longitude', 'id', 'veg_type', 'fmc_mean'])
df = df.set_index(['time', 'latitude', 'longitude']) 
for veg_type in [1,2,3]: # 1,2,3 correspond to vegetation types ID
    veg_type_mask = ndimage.generic_filter(veg_map.values==veg_type, np.all, footprint=np.ones((3,3), dtype=np.bool)) # pixel value == True if the pixel itself and all its neighbour pixels (3x3) are same veg type (either 1,2, or 3)
    #plt.imsave(f"/g/data/xc0/user/pablo/veg_t{veg_type}_mask.png", veg_type_mask[::10, ::10])

    veg_type_map = veg_map.where(veg_type_mask) # restrict veg mask to those pixels whose 3x3 pixels windows around them have all the same veg type ID 
    #print(np.sum(veg_type_map.values==veg_type))

    jj, ii = np.where(veg_type_map.values==veg_type) # define row (y, or lat) and column (x, or lon) indeces of pixels of one specific veg type (either 1, 2, or 3)
    n = 1000
    idxs = np.linspace(0, jj.shape[0] - 1, n, dtype=np.int) # define sub-selection of n evenly spaced indeces that will be used to extract FMC value

    for n, idx in enumerate(idxs):
        sample = ds.fmc_mean.isel(latitude=jj[idx], longitude=ii[idx]).to_dataframe() # all FMC values across time dimension at specified lat and lon
        sample['time'] = sample.index
        sample = sample.set_index(['time', 'latitude', 'longitude'])
        sample['veg_type'] = veg_type
        sample['id'] = f"{veg_type}_{n:03d}"
        df = df.append(sample)

    df.to_csv(f"modis_fmc_selection_{veg_type}.csv", index_label=['time', 'latitude', 'longitude'], float_format='%.4f')

df.to_csv("modis_fmc_selection.csv", index_label=['time', 'latitude', 'longitude'], float_format='%.4f')
