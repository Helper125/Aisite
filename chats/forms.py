from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Chat

User = get_user_model()

class Register_login(UserCreationForm):
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class ChatName(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["title"]


class ProfilEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ["photo_profil"]