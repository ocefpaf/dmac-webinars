import numpy as np
import scipy
import pandas as pd

from erddapy import ERDDAP

import micropip
await micropip.install("erddapy")

e = ERDDAP(
    server="NGDAC",
    protocol="tabledap",
    response="csv",
)

e.dataset_id = "whoi_406-20160902T1700"

e.variables = [
    "depth",
    "latitude",
    "longitude",
    "salinity",
    "temperature",
    "time",
]

e.constraints = {
    "time>=": "2016-09-03T00:00:00Z",
    "time<=": "2016-09-04T00:00:00Z",
    "latitude>=": 38.0,
    "latitude<=": 41.0,
    "longitude>=": -72.0,
    "longitude<=": -69.0,
}

# will fail
df = e.to_pandas()

url = e.get_download_url(response="csvp")
from pyodide.http import open_url
df = pd.read_csv(open_url(url))

import gsw
gsw.density.rho(df["salinity (1)"], df["temperature (Celsius)"], df["depth (m)"])