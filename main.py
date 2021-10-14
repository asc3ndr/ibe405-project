import requests
import pandas as pd

def fetch():

    # Kordinater til molde
    molde = "lat=62.73752&lon=7.15912"
    #Url for api
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?{molde}"
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    #Dict for å lagre data
    vær = {
    }

    response = requests.get(url, headers=headers)
    #Loop igjennom response
    for items in response.json().get("properties").get("timeseries"):
        temperatur = items["data"]["instant"]["details"]["air_temperature"]
        time = items["time"]
        #append to dict
        vær[time] = {"Temperatur": temperatur}

        #print(time[:10])

        """

        14.10.2021: {
            00:00:{
                temperatur
            },
            01:00: {
                temperatur
            }
        }

        """

    return vær

def write_to_csv(data):
    #cities = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
    for items in data:
        print(data)
        #Append til csv?
        vær = pd.DataFrame(data, data["temperatur"], columns = ["Dato", "Temperatur"])
        vær.to_csv('vær.csv')



if __name__ == "__main__":
    vær = fetch()
    print(vær)
    # write_to_csv(vær)
