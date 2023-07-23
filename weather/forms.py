from django.forms import ModelForm, TextInput
from .models import City
from .models import UserPreferences

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
        } #updates the input class to have the correct Bulma class and placeholder


class UserPreferencesForm(ModelForm):
    class Meta:
        model = UserPreferences
        fields = ['temperature_unit', 'wind_speed_unit', 'favorite_cities']