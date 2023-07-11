import logging
from typing import Any, Dict, Optional, Sequence, Tuple

import fsspec
import joblib
import xarray as xr
from datacube.model import Dataset
from datacube.utils.geometry import GeoBox
from deafrica_tools.classification import predict_xr
from odc.stats.plugins import StatsPluginInterface
from odc.stats.plugins._registry import register

from fmc_tools.feature_layer import s2_fmc_features

_log = logging.getLogger(__name__)


class PredS2FMC(StatsPluginInterface):
    """
    Prediction 
    """

    source_product = ["ga_s2am_ard_3", "ga_s2bm_ard_3"]
    target_product = "fmc_s2"

    def __init__(
        self,
        urls: Dict[str, Any],
        bands: Optional[Tuple] = None,
    ):
        # target band to be saved
        self.urls = urls
        self.bands = ("FMC")

    @property
    def measurements(self) -> Tuple[str, ...]:
        return self.bands

    def input_data(self, datasets: Sequence[Dataset], geobox: GeoBox) -> xr.Dataset:
        """
        Assemble the input data and do prediction here.

        """
        # create the features
        measurements = [
           "nbart_red",
            "nbart_green",
            "nbart_blue",
            "nbart_nir_1",
            "nbart_nir_2",
            "nbart_swir_2",
            "nbart_swir_3"
        ]

        input_data = s2_fmc_features(
            datasets, geobox, measurements
        )

        if not input_data:
            return None
        # read in model
        model = joblib.load(self.urls["model"]).set_params(n_jobs=1)

        # ------Run predictions--------
        # step 1: select features
        column_names=['ndvi','ndii','nbart_red','nbart_green','nbart_blue',
             'nbart_nir_1','nbart_nir_2','nbart_swir_2','nbart_swir_3']
        
        # reorder input data according to column names
        input_data = input_data[column_names]

        # step 2: prediction
        predicted = predict_xr(
            model=model,
            input_xr=input_data,
            clean=True,
            return_input=False,
        )
        
        predicted = predicted.rename({'Predictions': 'FMC'}).astype("float32")
        
        # rechunk on the way out
        return predicted.chunk({"x": -1, "y": -1})

    def reduce(self, xx: xr.Dataset) -> xr.Dataset:
        return predicted

register("Pred-S2-FMC", PredS2FMC)
