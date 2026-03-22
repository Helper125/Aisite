from django.contrib import admin
from django.urls import path
from .views import chats, register, login, logout, speak_messagge, profil_user, add_new_chat, edition_chat, edition_profil, delete_chat
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", chats, name="chat_list"),
    path("<int:chat_id>", chats, name="chat"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("speak_message<int:message_id>/", speak_messagge, name="speak_message"),
    path("profil/", profil_user, name="profil_user"),
    path("add_new_chat/", add_new_chat, name="add_new_chat"),
    path("edition_chat/<int:chat_id>/", edition_chat, name="edition_chat"),
    path("edition_profil/<str:username>/", edition_profil, name="edition_profil"),
    path("delete_chat<int:chat_id>/", delete_chat, name="delete_chat")
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)