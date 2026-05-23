import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

MY_LAT = 6.958547 # Your latitude
MY_LONG = 11.115951 # Your longitude

api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
PHONE_NUMBER = "+19129554115"
weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "cnt": 4,
}

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]["id"])
will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
        break
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {"http": os.environ["http_proxy"]}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It si going to rain today. Remember to bring on umbrella",
        from_=PHONE_NUMBER,
        to="+967774609057",
    )
    print(message.status)





