import numpy as np
import pandas as pd
from ioos_qc import qartod
from ioos_qc.config import QcConfig

import json

# Load QC config
def run_tests(df, variable):
    from pyodide.http import open_url
    config_file_path = "./qc_config.json"
    with open_url(config_file_path) as config_json:
        qc_config = json.load(config_json)

    qc = QcConfig(qc_config)
    qc_results = qc.run(
        inp=df[variable],
        tinp=df["timestamp"],
        zinp=df["z"],
    )

    qc_result_pd = pd.DataFrame(
        qc_results["qartod"], columns=qc_results["qartod"].keys()
    )
    result = pd.concat([df, qc_result_pd], axis=1)

    return result.set_index("time")


def make_mask(df, result, variable="sea_surface_height_above_sea_level", qc_test="spike_test"):
    obs = df[variable]
    mask = result[qc_test]

    return {
        "qc_pass": np.ma.masked_where(mask != 1, obs),
        "qc_suspect": np.ma.masked_where(mask != 3, obs),
        "qc_fail": np.ma.masked_where(mask != 4, obs),
        "qc_notrun": np.ma.masked_where(mask != 2, obs),
        }
