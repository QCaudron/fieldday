import json
from datetime import datetime

import pandas as pd
import requests


# Set some parameters for West Seattle
latitude = 47.549952
longitude = -122.354088
altitude = 93  # https://www.freemaptools.com/elevation-finder.htm
min_elevation = 30
start_date = "2023-06-21"
end_date = "2023-06-24"

# N2YO API details
BASE_URL = "https://api.n2yo.com/rest/v1/satellite/radiopasses"
PARAMETERS = f"{latitude}/{longitude}/{altitude}/10/{min_elevation}"

# FM satellites that might be more easily reachable than most
SATELLITE_IDS = {
    "ISS": 25544,
    "SO-50": 27607,
    "AO-91": 43017,
    "TEVEL-3": 50988,
    "TEVEL-4": 51063,
    "TEVEL-5": 50998,
    "PO-101": 43678,
}

# Columns for the output table
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


def get_satellite_passes(satellite: str, api_key: str) -> pd.DataFrame:
    """
    For a given satellite, get all passes around Field Day 2022.

    Parameters
    ----------
    satellite : str
        The human-legible short-hand satellite identifier, as in SATELLITE_IDS.
    api_key : str
        The API key for N2YO.

    Returns
    -------
    pd.DataFrame
        A dataframe of all satellite passes, cleaned up and with times in Pacific time.
    """

    # Format the API URL for this satellite
    norad_id = SATELLITE_IDS[satellite]
    url = f"{BASE_URL}/{norad_id}/{PARAMETERS}?apiKey={api_key}"

    # Query the API
    response = requests.get(url)
    response.raise_for_status()

    # Parse out the output
    data = json.loads(response.text)
    df = pd.DataFrame(data["passes"])

    # Round max elevation to the nearest int
    df["maxEl"] = df["maxEl"].round(0).astype(int)

    # Convert all times to Pacific time
    for col in ["startUTC", "maxUTC", "endUTC"]:
        df[col] = (
            pd.to_datetime(df[col], unit="s")
            .dt.tz_localize("UTC")
            .dt.tz_convert("US/Pacific")
        )

    # Keep only Field Day passes
    df = df.loc[(df["startUTC"] > start_date) & (df["endUTC"] < end_date)]

    # Format the datetimes to a clean string
    for col in ["startUTC", "maxUTC", "endUTC"]:
        df[col] = df[col].dt.strftime("%a %H:%M")

    # Clean up the dataframe -- add the satellite name and rename columns
    df["Satellite"] = satellite
    df = df.rename(columns=COLUMNS)[COLUMNS.values()]

    return df


if __name__ == "__main__":

    # Read in the API key
    with open("n2yo_api_key", "r") as f:
        api_key = f.read()

    # Grab passes for all satellites
    passes = []
    for satellite in SATELLITE_IDS.keys():
        passes.append(get_satellite_passes(satellite, api_key))

    # Concatenate passes and sort by time
    df = pd.concat(passes).sort_values("AOS Time")

    # Write a markdown file with sat passes
    with open("site/_static/satellite_template.md", "r") as f:
        template = (
            f.read()
            .replace("###passes###", df.to_markdown(index=False))
            .replace("###updated###", datetime.now().isoformat())
        )

    with open("site/schedule_and_activities/satellite.md", "w") as f:
        f.write(template)
