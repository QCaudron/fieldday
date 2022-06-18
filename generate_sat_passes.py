import json

import pandas as pd
import requests


latitude = 47.549952
longitude = -122.354088
altitude = 93  # https://www.freemaptools.com/elevation-finder.htm
min_elevation = 30

BASE_URL = "https://api.n2yo.com/rest/v1/satellite/radiopasses"
PARAMETERS = f"{latitude}/{longitude}/{altitude}/10/{min_elevation}"

SATELLITE_IDS = {
    "ISS": 25544,
    "SO-50": 27607,
    "AO-91": 43017,
    "PO-101": 43678,
    "AO-27": 22825
}

COLUMNS = {
    "Satellite": "Satellite",
    "startUTC": "AOS Time",
    "startAzCompass": "AOS Az",
    "maxUTC": "MOS Time",
    "maxAzCompass": "MOS Az",
    "maxEl": "MOS El",
    "endUTC": "LOS Time",
    "endAzCompass": "LOS Az",
}


def get_satellite_passes(satellite, api_key):

    norad_id = SATELLITE_IDS[satellite]
    url = f"{BASE_URL}/{norad_id}/{PARAMETERS}?apiKey={api_key}"

    response = requests.get(url)
    response.raise_for_status()

    data = json.loads(response.text)
    df = pd.DataFrame(data["passes"])

    df["maxEl"] = df["maxEl"].round(0).astype(int)

    for col in ["startUTC", "maxUTC", "endUTC"]:
        df[col] = (
            pd.to_datetime(df[col], unit="s")
            .dt.tz_localize("UTC")
            .dt.tz_convert("US/Pacific")
        )
    df = df.loc[(df["startUTC"] > "2022-06-24") & (df["endUTC"] < "2022-06-27")]
    for col in ["startUTC", "maxUTC", "endUTC"]:
        df[col] = df[col].dt.strftime("%a %H:%M")

    df["Satellite"] = satellite

    df = df.rename(columns=COLUMNS)[COLUMNS.values()]
    return df


if __name__ == "__main__":

    with open("n2yo_api_key", "r") as f:
        api_key = f.read()

    passes = []
    for satellite in SATELLITE_IDS.keys():
        passes.append(get_satellite_passes(satellite, api_key))

    df = pd.concat(passes).sort_values("AOS Time")

    with open("site/satellite.md", "w") as f:
        f.write("# Satellite passes\n\n")
        f.write((
            "Frequencies can be found on [Clint K6LCS's website]"
            "(https://www.work-sat.com/ewExternalFiles/WorkSat-12192021.pdf).\n\n"
        ))
        f.write("- AO-91 only in sunlight\n")
        f.write("- AO-27 active for ~4 minutes\n")
        f.write("- PO-101 [on a schedule](https://twitter.com/Diwata2PH)\n\n")
        f.write("## Passes\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n")