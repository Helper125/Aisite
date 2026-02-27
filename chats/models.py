from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Chat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    at_created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    is_ai = models.BooleanField(default=False)
    audio = models.FileField(null=True, blank=True, upload_to='voice/', default=None)
    at_created = models.DateTimeField(auto_now_add=True)
