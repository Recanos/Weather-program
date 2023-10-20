import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from django.contrib import messages

# Create your views here.
def index(request):
    API_key = '795e457b87c6d307d19165ae3f930411'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=" + API_key + '&units=metric' + '&lang=ru' +'&cnt=3'
    
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

        res = requests.get(url.format(city.name)).json()
        
        if res['cod'] == 200:
            city_info = {
                'city' : city.name,
                'temp' : res['main']['temp'],
                "icon" : res['weather'][0]['icon'],
                'wind' : res['wind']['speed'],

            }
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