import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from django.contrib import messages

import pytz
from datetime import datetime
t = pytz.timezone('Europe/Moscow')
moscow_current_datetime = str(datetime.now(t).time())[:2]


# Create your views here.
def index(request):
    API_key = '795e457b87c6d307d19165ae3f930411'
    url_1 = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=" + API_key + '&units=metric' + '&lang=ru'
    url_2 = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid=" + API_key + '&units=metric' + '&lang=ru' +'&cnt=8'
    
    flag_err = False
    flag_post = False


    if request.method=="POST":
        form_p = CityForm(request.POST)
        flag_post = True
        form_p.save()
    
    form_p = CityForm()

    cities = City.objects.all()

    all_cities = []
    for city in cities:

        res1 = requests.get(url_1.format(city.name)).json()
        res2 = requests.get(url_2.format(city.name)).json()

        print(res1)
        if res1['cod'] == 200:

            city_info = {
                'city' : city.name,
                'temp' : res1['main']['temp'],
                "icon" : res1['weather'][0]['icon'],
                'wind' : res1['wind']['speed'],
            }
            
            count = 0
            for i in range(res2['cnt']):
                if  int(res2['list'][i]['dt_txt'].split()[-1][:2]) > int(moscow_current_datetime):
                    city_info['temp_' + str(count)] = (res2['list'][i]['main']['temp'])
                    city_info['icon_' + str(count)] = (res2['list'][i]['weather'][0]['icon'])
                    city_info['time_' + str(count)] = (res2['list'][i]['dt_txt'].split()[-1][:-3])
                    count += 1
                    if count == 3:
                        break
                else:
                    continue

            print(city_info)
            if city_info in all_cities:
                City.objects.last().delete()
                flag_err = True
                mess = 'Город уже был!'
            else:
                all_cities.append(city_info)
        else:
            City.objects.last().delete()
            flag_err = True
            mess = "Введите правильное название города!"
            
    if flag_err and flag_post:
        messages.error(request, mess)
    elif flag_post and (not flag_err):
        messages.success(request, "Город добавлен!")

    context = {'all_form' : all_cities, 'form' : form_p}
    return render(request, 'weather/index.html', context)