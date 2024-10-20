from flask import Flask, render_template
from datetime import datetime
import requests
import json
import feedparser
app = Flask(__name__)

bnurl = "https://www.braunschweiger-zeitung.de/rss"  #Braunschweiger Zeitung
haqurl = "https://hnrss.org/frontpage"  #Hacker News
tagesurl = "https://www.tagesschau.de/index~rss2.xml"  # #Tagesschau

ddate = datetime.now().strftime('%d.%m.%Y - %H:%M Uhr')

#####JSON#####Wetter####10348 = BS
headers = {'Accept': 'application/json'}
r = requests.get('https://app-prod-ws.warnwetter.de/v30/stationOverviewExtended?stationIds=10348', headers=headers)
#with open('file.json') as f: #prop
#    r = json.load(f) #prop
station = json.loads(r.text)
#station = r #prop

for entry in station:
    fcast = station[entry]

fcast1 = fcast['forecast1']

unixt = int(fcast1['start'] / 1000)
print(unixt)
print(datetime.fromtimestamp(unixt).strftime('%d.%m.%Y, %H:%M:%S')) #stamp in ms


nowtime = datetime.now().strftime('%H') #aktuelle Stunde für Temperatureintrag
print(fcast1)

print("MAIN:",fcast1['temperature'][int(nowtime)])


actual_temperature = (fcast1['temperature'][int(nowtime)]) / 10
act_pressure = int(fcast1['surfacePressure'][int(nowtime)] / 10)
act_humidity = fcast1['humidity'][int(nowtime)] / 10
act_dewpoint = fcast1['dewPoint2m'][int(nowtime)] / 10 #nicht angezeigt

min_temp_today = fcast['days'][0]['temperatureMin'] / 10
max_temp_today = fcast['days'][0]['temperatureMax'] / 10

sunriset = datetime.fromtimestamp(fcast['days'][0]['sunrise'] / 1000).strftime('%H:%M')
sunsett = datetime.fromtimestamp(fcast['days'][0]['sunset'] / 1000).strftime('%H:%M')
windspeed = fcast['days'][0]['windSpeed'] / 10
wind_dir = fcast['days'][0]['windDirection']

if wind_dir == 0 or wind_dir <= 224:
    wind_h= 'N'
elif wind_dir >= 225 and wind_dir <= 449:
    wind_h = 'NNO'
elif wind_dir >= 450 and wind_dir <= 674:
    wind_h = 'NO'
elif wind_dir >= 675 and wind_dir <= 899:
    wind_h = 'ONO'
elif wind_dir >= 900 and wind_dir <= 1124:
    wind_h = 'O'
elif wind_dir >= 1125 and wind_dir <= 1149:
    wind_h = 'OSO'
elif wind_dir >= 1135 and wind_dir <= 1574:
    wind_h = 'SO'
elif wind_dir >= 1575 and wind_dir <= 1799:
    wind_h = 'SSO'
elif wind_dir >= 1800 and wind_dir <= 2024:
    wind_h = 'S'
elif 2025 >= wind_dir <= 2249:
    wind_h = 'SSW'
elif 2250 >= wind_dir <= 2474:
    wind_h = 'SW'
elif 2475 >= wind_dir <= 2699:
    wind_h = 'WSW'
elif 2700 >= wind_dir <= 2924:
    wind_h = 'W'
elif 2925 >= wind_dir <= 3149:
    wind_h = 'WNW'
elif 3150 >= wind_dir <= 3374:
    wind_h = 'NW'
elif 3375 >= wind_dir:
    wind_h = 'NNW'
else:
    wind_h = 'NaN'


@app.route('/')
def index():
    feed_bsnews = (feeder(bnurl))
    feed_hacknews = (feeder(haqurl))
    feed_tagesschau = (feeder(tagesurl))

    return render_template('index.html', actual_temperature=actual_temperature, act_pressure=act_pressure,
                          act_humidity=act_humidity, min_temp_today=min_temp_today,
                          max_temp_today=max_temp_today, sunriset=sunriset,
                          sunsett=sunsett, windspeed=windspeed,
                          wind_h=wind_h, nowtime=nowtime,
                          ddate=ddate, feed_bsnews=feed_bsnews,
                          feed_hacknews=feed_hacknews, feed_tagesschau=feed_tagesschau)


def feeder(entryfeed):
    read_feed = feedparser.parse(entryfeed)

    i = 0
    generated_feed = []
    for entry in read_feed.entries:
        i += 1
        generated_feed.append({'title': entry.title,
                           'link': entry.link})
    return generated_feed

if __name__ == '__main__':
    app.run(debug=True)
