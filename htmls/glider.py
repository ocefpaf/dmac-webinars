from datetime import date

import folium
import pandas as pd
from erddapy import ERDDAP
# from erddapy.url_handling import urlopen as open_url
from pyodide.http import open_url



today = date.today()


server = "https://gliders.ioos.us/erddap"
protocol = "tabledap"


e = ERDDAP(server=server, protocol=protocol)


kw = {
    "min_time": "now-1days",
}

search_url = e.get_search_url(response="csv", **kw)
search = pd.read_csv(open_url(search_url))
gliders = search["Dataset ID"].values.tolist()


def request_track(dataset_id):
    df = None
    protocol = "tabledap"
    variables = ["time", "longitude", "latitude"]
    # we will display only the glider's last teo week to reduce the data.
    constraints = {
        "time>=": "now-14days",
    }
    url = e.get_download_url(
        protocol=protocol,
        dataset_id=dataset_id,
        variables=variables,
        constraints=constraints,
        response="csvp",
        distinct=True,
    )
    try:
        df = pd.read_csv(open_url(url))
        df.name = dataset_id
    except Exception:
        pass
    return df


def request_info(dataset_id):
    info_url = e.get_info_url(dataset_id, response="csv")
    df = pd.read_csv(open_url(info_url))
    sub = df.loc[df["Variable Name"] == "NC_GLOBAL"]
    return sub.loc[sub["Attribute Name"] == "institution"]["Value"].squeeze()


all_datasets = {}
for glider in gliders:
    df = request_track(glider)
    institution = request_info(glider)
    all_datasets.update({glider: {"data": df, "institution": institution}})


def make_marker(dataset_id, dataset):
    df = dataset["data"]
    institution = dataset["institution"]
    link = f"{server}/" f"{protocol}/" f"{dataset_id}.html"
    popup = folium.Popup(
        html=f"""{institution} glider {dataset_id}""",
    )
    last_position = (
        df["latitude (degrees_north)"].iloc[-1],
        df["longitude (degrees_east)"].iloc[-1],
    )

    icon = folium.Icon(color="orange", icon="glyphicon glyphicon-plane")
    return folium.Marker(location=last_position, popup=popup, icon=icon)


tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}"
attr = "Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri"

m = folium.Map(tiles=tiles, attr=attr, png_enabled=False, zoom_control=False)

for glider, dataset in all_datasets.items():
    make_marker(glider, dataset).add_to(m)

m.fit_bounds(m.get_bounds())

m
