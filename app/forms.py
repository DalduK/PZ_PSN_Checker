from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

PLATFORMS = [('', ''), ('PS3', 'PlayStation 3'), ('PS4', 'PlayStation 4'), ('PSV', 'PlayStation Vita'),
             ('PSP', 'PlayStation Portable'), ('PS2', 'PlayStation 2'), ]


class ItemForm(forms.Form):
    item_title = forms.CharField(label='Item title', max_length=100)
    item_price = forms.FloatField(label='Price')
    image = forms.CharField(label='Item image', max_length=250)
    platform = forms.ChoiceField(choices=PLATFORMS)


class ItemFromURL(forms.Form):
    item_url = forms.CharField(label='URL gry', max_length=250)

class Search(forms.Form):
    szukaj = forms.CharField(label=False, max_length=250, required=False)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
