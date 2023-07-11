from typing import Any, Dict, List, Optional

import datacube
import xarray as xr
from odc.algo.io import load_with_native_transform
from pyproj import Proj, transform


def drop_nan_nodata(xx):
    """
    We pass this function to the
    native_transform parameter of
    load_with_native_transform in order
    to strip off the no-data values
    """
    for dv in xx.data_vars.values():
        if dv.attrs.get("nodata", "") == "NaN":
            dv.attrs.pop("nodata")
    return xx


def s2_fmc_features(
    datasets,
    geobox,
    measurements: List[str],
    dask_chunks: Dict[str, Any] = {"x": -1, "y": -1},
) -> Optional[xr.Dataset]:
    """
    Feature layer function for production run of
    S2 FMC.
    """

    ds = load_with_native_transform(
        datasets,
        geobox=geobox,
        native_transform=lambda x: drop_nan_nodata(x),
        bands=measurements,
        chunks=dask_chunks,
        resampling="bilinear",
    )
    
    ds['ndvi']=((ds.nbart_nir_1-ds.nbart_red)/(ds.nbart_nir_1+ds.nbart_red))
    ds['ndii']=((ds.nbart_nir_1-ds.nbart_swir_2)/(ds.nbart_nir_1+ds.nbart_swir_2))
    
    return ds.squeeze()
