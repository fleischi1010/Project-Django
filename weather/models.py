from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self): #show the actual city name on the dashboard
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    temperature_unit = models.CharField(max_length=10, choices=[('Celsius', 'Celsius'), ('Fahrenheit', 'Fahrenheit')])
    wind_speed_unit = models.CharField(max_length=10, choices=[('m/s', 'm/s'), ('mph', 'mph')])
    favorite_cities = models.ManyToManyField(City)

    def __str__(self):
        return f"Preferences for {self.user.username}"