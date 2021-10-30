import requests
import pandas as pd
import os.path
from datetime import datetime, timedelta, timezone
from pytz import timezone
import schedule
import time


def fetch():
    molde = "lat=62.73752&lon=7.15912"
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/complete?{molde}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    return response.json()


def oslo_time():
    oslo_tid = datetime.now().astimezone(timezone("Europe/Oslo"))
    oslo_tid = (oslo_tid - timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00Z")
    return oslo_tid

def prepare_data(data: dict):
    # Try to handle timezone difference on hosted server
    now = oslo_time()
    data = data["properties"]["timeseries"]

    # Find the forecast we wish to log
    for entry in data:
        if entry["time"] == now:
            data = entry["data"]["instant"]["details"]
            date, time = now.replace("Z", "").split("T")
            data["time"] = time
            data["date"] = date

    df = pd.DataFrame([data])

    # Change order of columns, setting time and date first.
    cols = df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    df = df[cols]

    return df

def append_to_csv(data: pd.DataFrame, path: str):
    # Only write header if the file does not already exist
    header = data.columns if not os.path.isfile(path) else False

    return data.to_csv(path, mode="a", header=header, index=False)

def is_time(path: str):
    #Check if there already is a row with current info
    df = pd.read_csv(path)
    result = oslo_time()
    result = result.split("T")
    date = result[0]
    time = result[1].replace("Z", "")

    return False if ((df["time"] == time) & (df["date"] == date)).any() else True


    # NOTE: Verify that the date and time isn't already in the csv file before fetching new data and appending.

def mainfunc():
    print("Checking!")

    run = is_time("test.csv")
    if run:
        data = fetch()
        data = prepare_data(data)
        append_to_csv(data=data, path="test.csv")
        print("Data has been added!")
    else:
        print("Has already been run!")

if __name__ == "__main__":
    mainfunc()
    schedule.every(30).minutes.do(mainfunc)


    while True:
        schedule.run_pending()
        time.sleep(10)
    # NOTE: Sleep? Schedule? Cron job? Some kind of event loop.
