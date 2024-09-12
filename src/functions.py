import json
import numpy as np
import pandas as pd
import requests
from janitor import clean_names

def load_week_stats(season, week, type_, session=None):
    """
    For testing
    season = 2020
    week = 5
    type_ = "rushing"
    session = requests.Session()
    """

    if week == 0:
        print(f"Loading {season} overall {type_} stats...")
    else:
        print(f"Loading {season} week {week} {type_} stats...")

    # max & min reg and post season weeks handling
    max_reg = 18 if season >= 2021 else 17 
    min_post = max_reg + 1
    max_post = min_post + 3

    # week and season types (i.e. REG || POST)
    if week == 0:
        path = f"https://appapi.ngs.nfl.com/statboard/{type_}?season={season}&seasonType=REG"
    elif 1 <= week <= max_reg:
        path = f"https://appapi.ngs.nfl.com/statboard/{type_}?season={season}&seasonType=REG&week={week}"
    elif min_post <= week <=max_post:
        path = f"https://appapi.ngs.nfl.com/statboard/{type_}?season={season}&seasonType=POST&week={week}"
    else:
        raise ValueError(f"Invalid week: {week}")

    # Spqwn a session
    if session is None:
        session = requests.Session()


    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) Apple WebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36",
        "Referer": session.headers.get("Referer", session.headers.get("Origin", "")),
    }

    resp = session.post(path, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"[ERROR]: {resp.status_code}")

    resp_json = resp.json()

    info = {k: v for k, v in resp.json.items() if not isinstance(v, list)}
    info_df = pd.DataFrame([info]).clean_names() # clean the column names

    print(info_df)


load_week_stats(2020, 5, "rushing", requests.Session())
