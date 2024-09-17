from django.shortcuts import render
from django.db.utils import IntegrityError
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .models import WeatherData, City
from . import config
from geopy.geocoders import Nominatim

import requests


class WeatherView(APIView):
    def get(self, request):
        city_names = request.query_params.get('cities', '').split(',')
        if not city_names:
            return Response({"error": "No city names provided."}, status=status.HTTP_400_BAD_REQUEST)
        city_names = [name.strip() for name in city_names if name.strip()]
        if not city_names:
            return Response({"error": "No valid city names provided."}, status=status.HTTP_400_BAD_REQUEST)
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        for city in city_names:
            lat, long = self.get_lat_long(city)
            City.objects.get_or_create(name=city, latitude=lat, longitude=long)
        cities = City.objects.filter(name__in=city_names)

        for city in cities:
            self.fetch_and_store_weather_data(city, start_time, end_time)

        weather_data = WeatherData.objects.filter(
            city__in=cities,
            timestamp__range=[start_time, end_time]
        ).values('city__name').annotate(
            average_temperature=Avg('temperature'),
            average_humidity=Avg('humidity')
        )

        if not weather_data:
            return Response({"error": "No weather data available after fetching."}, status=status.HTTP_404_NOT_FOUND)

        response_data = {}
        for index, city in enumerate(weather_data):
            print(cities[index].name, end_time.replace(second=0))
            current_data = WeatherData.objects.get(city=cities[index], timestamp=end_time.replace(second=0, microsecond=0))
            response_data[city['city__name']] = {
                "average_temperature": round(city['average_temperature'], 2),
                "average_humidity": round(city['average_humidity'], 2),
                "current_temp": current_data.temperature,
                "current_humidity": current_data.humidity
            }

        return Response(response_data, status=status.HTTP_200_OK)

    def get_lat_long(self, city_name):
        geolocator = Nominatim(user_agent="api")
        location = geolocator.geocode(city_name)
        return location.latitude, location.longitude

    def fetch_and_store_weather_data(self, city, start_time, end_time):
        start_time_str = start_time.strftime('%Y-%m-%dT%H:%M')
        end_time_str = end_time.strftime('%Y-%m-%dT%H:%M')
        url = "https://" + config.WEATHER_API_URL
        params = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "hourly": [config.TEMPERATURE, config.HUMIDITY],
            "timezone": config.TIME_ZONE,
            "start_hour": start_time_str,
            "end_hour": end_time_str,
        }
        response = requests.get(url, params=params)
        data = response.json()
        hourly_data = data.get('hourly', {})
        times = hourly_data.get('time', [])
        temperatures = hourly_data.get('temperature_2m', [])
        humidities = hourly_data.get('relative_humidity_2m', [])

        for time, temp, humidity in zip(times, temperatures, humidities):
            timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M")
            try:
                WeatherData.objects.create(city=city, timestamp=timestamp, temperature=temp, humidity=humidity)
            except IntegrityError:
                print(f"Skipping duplicate entry for timestamp: {timestamp}")
