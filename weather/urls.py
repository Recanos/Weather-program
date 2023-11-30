# WeatherApp.urls

from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:name_city>/', views.get_curr_info, name='weather-detail'),
    path('<str:name_city>/delete/', views.DeleteCurWR.as_view(), name='del_weather'),
    path('1/<str:name_city>/', views.get_info_1, name='weather_ch1'),
    path('2/<str:name_city>/', views.get_info_2, name='weather_ch2'),
    path('3/<str:name_city>/', views.get_info_3, name='weather_ch3'),
]