from django.contrib import admin
from django.urls import path
from .views import (chats, register, login, logout, speak_messagge, profil_user, add_new_chat, edition_chat, edition_profil, delete_chat,
                    chat_view, friends_list, delete_friend, add_user_in_chat, list_user_in_togetherChat, all_friends_request, accept_friend_request, unaccept_friend_request,
                    add_request_for_friend, add_new_togetherChat, edition_togetherChat, delete_togetherChat) 
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
    path("delete_chat<int:chat_id>/", delete_chat, name="delete_chat"),
    path("together_chat<int:chat_id>/", chat_view, name="chat_view"),
    path("friends-list/", friends_list, name="friends-list"),
    path("friend-delete<int:friend_id>/", delete_friend, name="delete-friend"),
    path("add-user-in-chat<int:chat_id>/", add_user_in_chat, name="add-user-in-chat"),
    path("list_user_in_togetherChat<int:chat_id>/", list_user_in_togetherChat, name="list_user_in_togetherChat"),
    path("all_friends_request/", all_friends_request, name="all_friends_request"),
    path("accept_friend_request<int:request_id>/", accept_friend_request, name="accept_friend_request"),
    path("unaccept_friend_request<int:request_id>/", unaccept_friend_request, name="unaccept_friend_request"),
    path("add_request_for_friend<int:user_id>", add_request_for_friend, name="add_request_for_friend"),
    path("add_new_togetherChat", add_new_togetherChat, name="add_new_togetherChat"),
    path("edition_togetherChar<int:chat_id>", edition_togetherChat, name="edition_togetherChat"),
    path("delete_togetherChat<int:chat_id>", delete_togetherChat, name="delete_togetherChat")
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)