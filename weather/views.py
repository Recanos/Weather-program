import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy

import pytz
from datetime import datetime
t = pytz.timezone('Europe/Moscow')
moscow_current_datetime = str(datetime.today()).split()

global API_key, url_1, url_2
API_key = '795e457b87c6d307d19165ae3f930411'
url_1 = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=" + API_key + '&units=metric' + '&lang=ru'
url_2 = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid=" + API_key + '&units=metric' + '&lang=ru' +'&cnt=35'

def get_curr_info(request, name_city):

    glavn = []

    if  len(City.objects.filter(name=name_city)) == 0:
        return HttpResponseNotFound("Город не существует!")
    res2 = requests.get(url_2.format(name_city)).json()
    data = ""
    for i in res2['list']:
        dt = dict()
        if moscow_current_datetime[0] == i['dt_txt'].split()[0]:
            dt['time'] = i['dt_txt'].split()[1][:-3]
            dt['descr'] = i['weather'][0]['description']
            dt['temp'] = i['main']['temp']
            dt['icon'] = i['weather'][0]['icon']
            glavn.append(dt)
            data = i['dt_txt'].split()[0][-2:] + i['dt_txt'].split()[0][-6:-2] + i['dt_txt'].split()[0][:4]
        elif moscow_current_datetime[0] > i['dt_txt'].split()[0]:
            continue
        else:

            break

    context = {'city' : name_city,
                'all_dt' : glavn,
                'date' : data,
                }
    return render(request, 'weather/weather_view.html', context)

def get_info_1(request, name_city):

    glavn = []

    if  len(City.objects.filter(name=name_city)) == 0:
        return HttpResponseNotFound("Город не существует!")
    res2 = requests.get(url_2.format(name_city)).json()

    k = 0
    need = moscow_current_datetime[0]
    data = ""
    for i in res2['list']:
        dt = dict()
        if need == i['dt_txt'].split()[0] and k == 1:
            dt['time'] = i['dt_txt'].split()[1][:-3]
            dt['descr'] = i['weather'][0]['description']
            dt['temp'] = i['main']['temp']
            dt['icon'] = i['weather'][0]['icon']
            glavn.append(dt)
        elif need < i['dt_txt'].split()[0]:
            k += 1
            if k == 1:
                data = i['dt_txt'].split()[0][-2:] + i['dt_txt'].split()[0][-6:-2] + i['dt_txt'].split()[0][:4]
                dt['time'] = i['dt_txt'].split()[1][:-3]
                dt['descr'] = i['weather'][0]['description']
                dt['temp'] = i['main']['temp']
                dt['icon'] = i['weather'][0]['icon']

                glavn.append(dt)

                need = i['dt_txt'].split()[0]
            else:
                break

    context = {'city' : name_city,
                'all_dt' : glavn,
                'date' : data,
                }
    return render(request, 'weather/weather_view.html', context)

def get_info_2(request, name_city):

    glavn = []

    if  len(City.objects.filter(name=name_city)) == 0:
        return HttpResponseNotFound("Город не существует!")
    res2 = requests.get(url_2.format(name_city)).json()

    k = 0
    need = moscow_current_datetime[0]
    data = ""
    for i in res2['list']:
        dt = dict()
        if need == i['dt_txt'].split()[0] and k == 2:
            dt['time'] = i['dt_txt'].split()[1][:-3]
            dt['descr'] = i['weather'][0]['description']
            dt['temp'] = i['main']['temp']
            dt['icon'] = i['weather'][0]['icon']
            glavn.append(dt)
        elif need < i['dt_txt'].split()[0]:
            k += 1
            need = i['dt_txt'].split()[0]
            if k == 2:
                data = i['dt_txt'].split()[0][-2:] + i['dt_txt'].split()[0][-6:-2] + i['dt_txt'].split()[0][:4]
                dt['time'] = i['dt_txt'].split()[1][:-3]
                dt['descr'] = i['weather'][0]['description']
                dt['temp'] = i['main']['temp']
                dt['icon'] = i['weather'][0]['icon']

                glavn.append(dt)
            elif k == 3:
                break

    context = {'city' : name_city,
                'all_dt' : glavn,
                'date' : data,
                }
    return render(request, 'weather/weather_view.html', context)

def get_info_3(request, name_city):

    glavn = []

    if  len(City.objects.filter(name=name_city)) == 0:
        return HttpResponseNotFound("Город не существует!")
    res2 = requests.get(url_2.format(name_city)).json()

    k = 0
    need = moscow_current_datetime[0]
    data = ""
    for i in res2['list']:
        dt = dict()
        if need == i['dt_txt'].split()[0] and k == 3:
            dt['time'] = i['dt_txt'].split()[1][:-3]
            dt['descr'] = i['weather'][0]['description']
            dt['temp'] = i['main']['temp']
            dt['icon'] = i['weather'][0]['icon']
            glavn.append(dt)
        elif need < i['dt_txt'].split()[0]:
            k += 1
            need = i['dt_txt'].split()[0]
            if k == 3:
                data = i['dt_txt'].split()[0][-2:] + i['dt_txt'].split()[0][-6:-2] + i['dt_txt'].split()[0][:4]
                dt['time'] = i['dt_txt'].split()[1][:-3]
                dt['descr'] = i['weather'][0]['description']
                dt['temp'] = i['main']['temp']
                dt['icon'] = i['weather'][0]['icon']

                glavn.append(dt)
            elif k == 4:
                break

    context = {'city' : name_city,
                'all_dt' : glavn,
                'date' : data,
                }
    return render(request, 'weather/weather_view.html', context)

class DeleteCurWR(DeleteView):
    model = City
    template_name = 'weather/index.html'
    success_url = reverse_lazy('weather:index')  # Redirect to the 'index' view

    def get_object(self, queryset=None):
        # Retrieve the City object based on the name_city parameter in the URL
        return self.model.objects.get(name=self.kwargs['name_city'])

def start(request):
    context = {'title' : 'Welcome!'}
    return render(request, 'weather/start.html', context)

def index(request):
    flag_err = False
    flag_post = False

    if request.method=="POST":
        form_p = CityForm(request.POST)
        flag_post = True
        form_p.save()
    
    form_p = CityForm()

    if len(City.objects.all()) > 5:
        City.objects.last().delete()
        flag_err = True
        mess = 'Максимум можно отслеживать 5 городов!'
            
    cities = City.objects.all()

    all_cities = []

    for city in cities:

        res1 = requests.get(url_1.format(city.name)).json()
        res2 = requests.get(url_2.format(city.name)).json()
        if res1['cod'] == 200:
        
            city_info = {
                'city' : city.name,
                'temp' : round(res1['main']['temp']),
                "icon" : res1['weather'][0]['icon'],
                'wind' : round(res1['wind']['speed'], 1),
            }
            
            count = 0
            max_temp = -100
            icon = ""
            dat = ""
            list_dt = []
            for i in range(res2['cnt']):
                if  (moscow_current_datetime[0]) < (res2['list'][i]['dt_txt'].split()[0]):
                    if res2['list'][i]['dt_txt'].split()[0][-2:] not in list_dt:
                        if len(list_dt) > 0:
                            city_info['temp_' + str(count)] = max_temp
                            city_info['icon_' + str(count)] = icon
                            city_info['time_' + str(count)] = dat
                        list_dt.append(res2['list'][i]['dt_txt'].split()[0][-2:])
                        dat = ".".join([res2['list'][i]['dt_txt'].split()[0][-2:], res2['list'][i]['dt_txt'].split()[0][-5:-3]])
                        
                        count += 1
                        if count == 4:
                            break
                        max_temp = -100
                        icon = ""

                    if res2['list'][i]['main']['temp'] > max_temp:
                        max_temp = round(res2['list'][i]['main']['temp'])
                        icon = res2['list'][i]['weather'][0]['icon']
  

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