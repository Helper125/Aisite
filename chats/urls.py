from django.contrib import admin
from django.urls import path
from .views import chats, register, login, logout, speak_messagge
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", chats, name="chat"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("speak_message<int:message_id>/", speak_messagge, name="speak_message")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)