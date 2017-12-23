# Developer : Hamdy Abou El Anein

from pyIslam.praytimes import PrayerConf, Prayer
from pyIslam.hijri import HijriDate
from pyIslam.qiblah import Qiblah
from datetime import date
from easygui import *
import webbrowser
import sys


isworld = "./images/IslamicWorld.gif"
islamic = "./images/islamic.gif"


image = islamic
msg = "                      Welcome to Islamic-Prayer\n\n\n This software will open two pages on your web browser to help you to find your latitude, longitude and your timezone"
choices = ["Continue"]
reply = buttonbox(msg, image=image, choices=choices)

if reply == "Continue":
    webbrowser.open("https://www.latlong.net/")
    webbrowser.open("https://www.timeanddate.com/time/map/")
    msg = "Enter the latitude and longitude of your city and the timezone (GMT+n)"
    title = "Islamic Prayer"
    fieldNames = ["Latitude", "Longitude","Timezone Ex. : GMT+1 = 1"]
    fieldValues = []
    fieldValues = multenterbox(msg, title, fieldNames)

elif reply == "./images/islamic.gif":
    webbrowser.open("https://www.latlong.net/")
    webbrowser.open("https://www.timeanddate.com/time/map/")
    msg = "Enter the latitude and longitude of your city and the timezone (GMT+n)"
    title = "Islamic Prayer"
    fieldNames = ["Latitude", "Longitude","Timezone Ex. : GMT+1 = 1"]
    fieldValues = []
    fieldValues = multenterbox(msg, title, fieldNames)


else:
    sys.exit(0)


longitude = fieldValues[1]

if longitude == '':
    longitude = 3.250000
    latitude = 36.716667
    timezone = 1
    fajr_isha_method = 3
    asr_fiqh = 1
else:
    longitude = float(longitude)
    latitude = float(fieldValues[0])
    timezone = float(fieldValues[2])


    msg = "Choose the Fajr and Ishaa reference\n\n1 = University of Islamic Sciences, Karachi\n2 = Muslim World League\n3 = Egyptian General Authority of Survey\n4 = Umm al-Qura University, Makkah\n5 = Islamic Society of North America"
    title = "Islamic Prayer"
    fieldNames = ["Enter your choice (from 1 to 5)"]
    fieldValues = []
    fieldValues = multenterbox(msg, title, fieldNames)

    fajr_isha_method = int(fieldValues[0])


    msg = "Choose the Asr Madhab\n\n1 = Shafii\n2 = Hanafi"
    title = "Islamic Prayer"
    fieldNames = ["Enter your choice (from 1 or 2)"]
    fieldValues = []
    fieldValues = multenterbox(msg, title, fieldNames)

    asr_fiqh = int(fieldValues[0])

pconf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)

pt = Prayer(pconf, date.today())
hijri = HijriDate.today()

0

image = isworld
msg = "Prayer Times\n\nFajr:    " + str(pt.fajr_time())+str("\nSherook: " + str(pt.sherook_time()))+str("\nDohr:    " + str(pt.dohr_time()))+str("\nAsr:     " + str(pt.asr_time()))+str("\nMaghreb: " + str(pt.maghreb_time()))+str("\nIshaa:   " + str(pt.ishaa_time()))+str("\n\nQiblah direction from the north: " + Qiblah(pconf).sixty())
choices = ["Ok"]
reply = buttonbox(msg, image=image, choices=choices)
