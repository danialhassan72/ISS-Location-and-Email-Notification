import requests
from datetime import datetime
import smtplib
import time


MY_EMAIL = "your_email"
MY_PASSWORD = "Your_14_digit_password"
MY_LAT =  33.684422
MY_LNG = 73.047882


def get_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return iss_latitude,iss_longitude

def is_iss_overhead():
    iss_latitude, iss_longitude = get_iss_position()
    if MY_LAT - 5 <= iss_latitude <= MY_LAT +5 and MY_LNG -5 <= iss_longitude <= MY_LNG +5:
        return True
# {'results': {'sunrise': '12:18:08 AM', 'sunset': '2:10:16 PM', 'solar_noon': '7:14:12 AM', 'day_length'
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    # print(data)
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[1])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[1])
    print(sunrise)
    print(sunset)
    #
    time_now = datetime.now().hour
    if time_now >= sunset or time_now<= sunrise:
        return True

while True:

    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="where you want to send the email",
            msg="Subject: Look UP! \n\n The ISS is above you in the sky!!!"
        )
        time.sleep(60)
