from django import forms
from .models import Availability, Profile, Activity
from django.contrib.auth.models import User


class AvailabilityForm(forms.ModelForm):
    start = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}),
                                input_formats=['%Y-%m-%dT%H:%M'])
    end = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}),
                              input_formats=['%Y-%m-%dT%H:%M'])
    activity = forms.ModelChoiceField(queryset=Activity.objects.all())

    class Meta(object):
        model = Availability
        fields = ['start', 'end', 'activity']


class ActivityForm(forms.ModelForm):

    class Meta(object):
        model = Activity
        fields = '__all__'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta(object):
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta(object):
        model = User
        fields = ['username', 'password']
