from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class Register_login(UserCreationForm):
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]