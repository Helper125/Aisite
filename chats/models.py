from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

class Users(AbstractUser):
    username = models.CharField(blank=True, max_length=100, unique=True)
    photo_profil = models.ImageField(blank=True, upload_to="media/", default="media/defaul_photo_user_rNZvkqC.png")
    at_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='receiver_requests')
    accepted = models.BooleanField(default=False)
    unaccepted = models.BooleanField(default=False)
    wait = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}"


class Friend(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user}"


class Chat(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, default="Keine")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    at_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} --- {self.user}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    is_ai = models.BooleanField(default=False)
    audio = models.FileField(null=True, blank=True, upload_to='voice/', default=None)
    at_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chat}"


class TogetherChat(models.Model):
    title = models.CharField(max_length=400)
    user = models.ManyToManyField(Users)
    owner = models.ForeignKey(Users, null=True, on_delete=models.CASCADE, related_name='owner_chat')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class MessageInChat(models.Model):
    chat = models.ForeignKey(TogetherChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    file = models.FileField(upload_to='attachments/%Y/%m/5d/', null=True, blank=True)
    for_AI = models.BooleanField(default=False)
    is_AI = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chat} --- {self.sender} --- {self.created_at} --- {self.for_AI}"