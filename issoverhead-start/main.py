import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv

load_dotenv()
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude
MY_EMAIl = os.getenv('MY_EMAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')

#Your position is within +5 or -5 degrees of the ISS position.
def is_iss_overhead():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")

    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT + 5 >= iss_latitude >= MY_LAT -5 and MY_LONG + 5 >= iss_longitude >= MY_LONG -5:
        return True

def is_currently_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    # print(sunrise)

    time_now = datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_currently_dark():
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(MY_EMAIl, MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIl,
                            to_addrs=MY_EMAIl,
                            msg="Subject: Look Up\n\n The ISS is above you in the sky"
                            )



#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



