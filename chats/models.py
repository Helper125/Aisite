from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

class Users(AbstractUser):
    username = models.CharField(blank=True, max_length=100, unique=True)
    photo_profil = models.ImageField(blank=True, upload_to="media/", default="media/defaul_photo_user_rNZvkqC.png")
    at_created = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, default="Keine")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    at_created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    is_ai = models.BooleanField(default=False)
    audio = models.FileField(null=True, blank=True, upload_to='voice/', default=None)
    at_created = models.DateTimeField(auto_now_add=True)
