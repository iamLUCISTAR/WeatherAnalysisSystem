from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.WeatherView.as_view(), name="test"),
    path('search/', views.weather_search_view, name='weather-search'),
]
