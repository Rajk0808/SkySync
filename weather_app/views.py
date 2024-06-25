from django.shortcuts import render 
from django.http import HttpResponse
import datetime
import requests

# Create your views here.

def index(request):
    #API_KEY ='d0683a7a1bb54701a0b111626242305'
    current_weather_url = 'http://api.weatherapi.com/v1/current.json?key=d0683a7a1bb54701a0b111626242305&q={}'
    forecast_url = 'http://api.weatherapi.com/v1/forecast.json?key=d0683a7a1bb54701a0b111626242305&q={}&days=5'

    if request.method == 'POST':
        city1 = request.POST.get('city1', None)
        city2 = request.POST.get('city2', None)
        weather_data1 , daily_forecast1 = fetch_weather_and_forecast(city1, current_weather_url, forecast_url)
        if city2 :
            weather_data2 , daily_forecast2 = fetch_weather_and_forecast(city2, current_weather_url, forecast_url)

        else :
            weather_data2 , daily_forecast2 = None , None   


        context = {
            'weather_data1' : weather_data1,
            'daily_forecast1' :  daily_forecast1,
            'weather_data2' : weather_data2,
            'daily_forecast2' : daily_forecast2
            }
        #print("\ncontext",context)
        return render(request , 'index.html' , context)         
    else :
         return render(request , 'index.html')

def fetch_weather_and_forecast(city ,current_weather_url, forecast_url):
    
    
    forecast_response = requests.get(forecast_url.format(city)).json()

    
    current_response = requests.get(current_weather_url.format(city)).json()
    

    current_weather = current_response.get('current')
    weather_data = {
    
        'city': city,
        'temperature' : current_weather.get('temp_c'),
        'description' : current_weather.get('condition', {}).get('text'),
        'icon' : current_weather.get('condition', {}).get('icon')
    }

    daily_forecast = []
    if 'forecast' in forecast_response and 'forecastday' in forecast_response['forecast']:
            for daily_data in forecast_response['forecast']['forecastday'][:5]:
                daily_forecast.append({
                    'day': datetime.datetime.strptime(daily_data['date'], '%Y-%m-%d').strftime('%A'),
                    'min_temp': daily_data['day']['mintemp_c'],
                    'max_temp': daily_data['day']['maxtemp_c'],
                    'description': daily_data['day']['condition']['text'],
                    'icon': daily_data['day']['condition']['icon']
                })

    return weather_data , daily_forecast  

