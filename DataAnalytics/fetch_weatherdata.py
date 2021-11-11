import requests
from datetime import datetime, timedelta, timezone
from pytz import timezone
import schedule
import time

from db import DB

# Get weatherdata
def fetch():
    molde = "lat=62.73752&lon=7.15912"
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/complete?{molde}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    return response.json()


# Return the current Oslo time
def oslo_time():
    oslo_tid = datetime.now().astimezone(timezone("Europe/Oslo"))
    oslo_tid = (oslo_tid - timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00Z")
    return oslo_tid


# Format dataentry
def prepare_data(data: dict):
    # Try to handle timezone difference on hosted server
    now = oslo_time()
    data = data["properties"]["timeseries"]

    # Find the forecast we wish to log
    for entry in data:
        if entry["time"] == now:
            data = entry["data"]["instant"]["details"]
            date, time = now.replace("Z", "").split("T")
            data["_id"] = entry["time"]
            data["time"] = time
            data["date"] = date
            return data
    return None


# Create scheduled job
def job():
    weatherDB = DB()
    data = fetch()
    data = prepare_data(data)

    if not weatherDB.get(oslo_time()):
        return weatherDB.create(data)
    return None


if __name__ == "__main__":

    job()
    schedule.every(30).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(10)
