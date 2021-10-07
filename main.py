import requests
import pandas as pd
# from metno_locationforecast import place, Forecast
# https://github.com/Rory-Sullivan/metno-locationforecast/blob/master/examples/basic_usage.py

def fetch():
    #https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=62.73752&lon=7.15912


    # Kordinater til molde
    molde = "lat=62.73752&lon=7.15912"
    #Url for api
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?{molde}"
    #Dict for å lagre data
    vær = {
    }

    #403 forbidden
    response = requests.get(url)

    #Loop igjennom response
    for items in response.json():
        #Temp hardcode
        dato = "07.10.2020"
        temperatur = 12

        #append to dict
        vær[dato] = {"Temperatur": temperatur}
    return vær

def write_to_csv(data):
    #data = vær dict


    #cities = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
    for items in data:
        #Append til csv?
        vær = pd.DataFrame(data["dato"], data["temperatur"], columns = ["Dato", "Temperatur"])
        vær.to_csv('vær.csv')



if __name__ == "__main__":
    print(fetch())
