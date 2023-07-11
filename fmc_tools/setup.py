#!/usr/bin/env python3

import io
import os
from setuptools import find_packages, setup

# Where are we?
IS_DEA_SANDBOX = ('sandbox' in os.getenv('JUPYTER_IMAGE', default=''))

# What packages are required for this module to be executed?
REQUIRED = [
    "xarray",
    "joblib",
    "numba",
    "numpy",
    "datacube",
    "pyproj",
    "fsspec",
    "odc-stats",
    "odc-stac",
    "odc-io",
    "odc-algo",
    "odc-dscache",
    "pandas",
    "typing",
    "geopandas",
    "gdal",  
    "scipy",
    "dask",
    "dask-ml",
    "geopy",
    # DE Africa tools from https://github.com/digitalearthafrica/deafrica-sandbox-notebooks/tree/main/Tools
    "dea_tools",
]

# Package meta-data.
NAME = "fmc_tools"
DESCRIPTION = "Tools for S2 FMC over Australia"
URL = ""
EMAIL = "chad.burton@ga.gov.au"
AUTHOR = "Digital Earth Australia"
REQUIRES_PYTHON = ">=3.6.0"

# Import the README and use it as the long-description.
here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup_kwargs = {
    "name": NAME,
    "version": "1.0.0",
    "description": DESCRIPTION,
    "long_description": long_description,
    "author": AUTHOR,
    "author_email": EMAIL,
    "python_requires": REQUIRES_PYTHON,
    "url": URL,
    "install_requires": REQUIRED if not IS_DEA_SANDBOX else [],
    "packages": find_packages(),
    "include_package_data": True,
    "license": "Apache License 2.0",
    "entry_points": {
        "console_scripts": [
            "fmc-task = fmc_tools.geojson_defined_tasks:main",
        ]
    },
}

setup(**setup_kwargs)
