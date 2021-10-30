import json
import requests
import pandas as pd
from json import dump


def fetch():
    molde = "lat=62.73752&lon=7.15912"
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?{molde}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    return response.json()


def write_to_csv(data):
    # cities = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
    for items in data:
        print(data)
        # Append til csv?
        vær = pd.DataFrame(data, data["temperatur"], columns=["Dato", "Temperatur"])
        vær.to_csv("vær.csv")


data = fetch()
df = pd.json_normalize(data)
# df = pd.read_json(data)
# df.to_csv("data.csv")
print(df)


# with open("data.json", "w") as outfile:
#     json.dump(data, outfile)

