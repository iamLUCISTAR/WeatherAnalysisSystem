from django.db import models


class City(models.Model):
    """
    Database model to store city data
    """
    name = models.CharField(unique=True, max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()


class WeatherData(models.Model):
    """
    Database model to store weather data
    """
    city = models.ForeignKey(City, related_name='weather_data', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    temperature = models.FloatField()
    humidity = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['city', 'timestamp'], name='unique_city_timestamp')
        ]


