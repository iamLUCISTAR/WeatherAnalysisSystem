from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.WeatherView.as_view(), name="test")
]
