from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message, FriendRequest, Friend, TogetherChat, MessageInChat
from django.contrib.auth.decorators import login_required
from .forms import Register_login, ChatName, ProfilEdit, TogetherChatName
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .Ais import artificial_intelligence
import speech_recognition as sr
from gtts import gTTS
import os
from django.conf import settings
from django.http import FileResponse
from langdetect import *
from django.contrib.auth import get_user_model
import random

User = get_user_model()


# Create your views here.

@login_required
def chats(request, chat_id=None):
    all_chats = Chat.objects.filter(user=request.user)
    if not all_chats.exists():
        chat = Chat.objects.create(user=request.user, title="zuerst")
    else:
        if chat_id:
            chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        else:
            chat = all_chats.first()
    message = Message.objects.filter(chat=chat).order_by("at_created")

    recognized_text = None

    if request.method == "POST":
        message_text = request.POST.get("message_text")
        file = request.FILES.get("file")
        if request.FILES.get('audio_file'):
            audio_file = request.FILES['audio_file']

            languages = ("uk-UA", "en-US", "de-DE")

            with open("temp_audio.wav", "wb+") as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            recognizer = sr.Recognizer()
            with sr.AudioFile("temp_audio.wav") as source:
                audio_data = recognizer.record(source)
                try:
                    recognizer_text = recognizer.recognize_amazon(audio_data, language=languages)
                except sr.UnknownValueError:
                    recognized_text = "error"
                except sr.RequestError as e:
                    recognized_text = f"error {e}"



        ai_message = artificial_intelligence(message_text, file)

        create = Message.objects.create(text=message_text, chat=chat, file=file)
        create_ai = Message.objects.create(text=ai_message, chat=chat, is_ai=True)

        

        return redirect("chat", chat_id=chat_id)

    return render(request, "chat.html", {"chat":chat, "message":message, "recognized_text":recognized_text})


def speak_messagge(request, message_id):
    message = Message.objects.get(id=message_id)

    if not message.audio:
        lang_detect = detect(message.text)

        tts = gTTS(text=message.text, lang=lang_detect)
        file_path = f"voice/voice{message_id}.mp3"
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        tts.save(full_path)

        message.audio.name = file_path
        message.save()

        return redirect("chat", chat_id=message.chat.id)


def register(request):
    if request.method == "POST":
        form = Register_login(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("/")
        
    else:
        form = Register_login()
    return render(request, "user/register.html", {"form":form})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            return redirect("login")
    return render(request, "user/login.html")


def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def profil_user(request):
    profil = User.objects.get(username=request.user.username)

    all_chats = Chat.objects.filter(user=request.user)

    all_group = TogetherChat.objects.filter(user__in=[request.user])
        

    return render(request, 'profil.html', {'profil':profil, "all_chats":all_chats, "all_group":all_group})


def add_new_chat(request):
    chat = Chat.objects.create(user=request.user, title="None")

    return redirect("profil_user")


@login_required
def edition_chat(request, chat_id):
    edit_chat = get_object_or_404(Chat, id=chat_id)

    if request.method == "POST":
        form = ChatName(request.POST, instance=edit_chat)
        if form.is_valid():
            form.save()
            return redirect("profil_user")
    else:
        form = ChatName(instance=edit_chat)
    
    return render(request, "form.html", {"form":form})


@login_required
def edition_profil(request, username):
    edit_profil = get_object_or_404(User, username=username)

    if request.method == "POST":
        form = ProfilEdit(request.POST, request.FILES, instance=edit_profil)
        if form.is_valid():
            form.save()
            return redirect("profil_user")
    else:
        form = ProfilEdit(instance=edit_profil)
    
    return render(request, "profil_form.html", {"form":form})


@login_required
def delete_chat(request, chat_id):
    del_chat = get_object_or_404(Chat, id=chat_id)

    del_chat.delete()

    return redirect("profil_user")


@login_required
def add_request_for_friend(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    add = FriendRequest.objects.create(sender=request.user, receiver=receiver)

    return redirect("friends-list")


@login_required
def all_friends_request(request):

    alls = FriendRequest.objects.filter(receiver=request.user, wait=True)

    return render(request, "all_friends_request.html", {"alls":alls})


@login_required
def accept_friend_request(request, request_id):
    fr = FriendRequest.objects.get(id=request_id)

    if fr.receiver == request.user:
        fr.accepted = True
        fr.wait = False
        fr.save()

        Friend.objects.create(user=fr.sender, friend=fr.receiver)
        Friend.objects.create(user=fr.receiver, friend=fr.sender)

    return redirect("all_friends_request")
'''добавити все по стилям, зробити кнопку "створити новий чат", зробити кнопку "редагувати назву чату"'''

@login_required
def unaccept_friend_request(request, request_id):
    fr = FriendRequest.objects.get(id=request_id)

    fr.unaccepted = True
    fr.wait = False
    fr.save()

    return redirect("all_friends_request")


@login_required
def friends_list(request):
    friends = Friend.objects.filter(user=request.user)

    friends_ids = friends.values_list('friend__id', flat=True)

    requests = FriendRequest.objects.filter(sender=request.user)
    requests_ids = requests.values_list("receiver__id", flat=True)

    friends_search = ''
    if 'query' in request.GET:
        query = request.GET["query"]
        friends_search = User.objects.filter(username__iregex=query)

    return render(request, "friends_list.html", {"friends":friends, "friends_search":friends_search, "friends_ids":friends_ids, "requests_ids":requests_ids})


def delete_friend(request, friend_id):
    deletes = get_object_or_404(Friend, id=friend_id)
    friend_fr = Friend.objects.filter(user=deletes.friend, friend=deletes.user).delete()

    deletes.delete()

    return redirect("friends-list")


def add_new_togetherChat(request):
    create = TogetherChat.objects.create(title="Jackman AI Chat", owner=request.user)
    create.user.add(request.user)

    return redirect("profil_user")


@login_required
def chat_view(request, chat_id):
    chat = get_object_or_404(TogetherChat, id=chat_id)

    if not request.user in chat.user.all():
        return redirect("/")

    if request.method == "POST":
        message_text = request.POST.get("message_text")
        file = request.FILES.get("file")

        if message_text or file:
            MessageInChat.objects.create(
                chat=chat,
                sender=request.user,
                text=message_text,
                file=file
            )
        return redirect("chat_view", chat_id=chat_id)

    message = MessageInChat.objects.filter(chat=chat)

    return render(request, "togetherChat.html", {
        "chat": chat,
        "message": message
    })

def edition_togetherChat(request, chat_id):
    edit_chat = get_object_or_404(TogetherChat, id=chat_id)

    if request.method == "POST":
        form = TogetherChatName(request.POST, instance=edit_chat)
        if form.is_valid():
            form.save()
            return redirect("profil_user")
    else:
        form = TogetherChatName(instance=edit_chat)

    return render(request, "edit_togetherChat_name.html", {"form":form})


def delete_togetherChat(request, chat_id):
    delete_ch = get_object_or_404(TogetherChat, id=chat_id)
    
    delete_ch.delete()

    return redirect("profil_user")


def add_user_in_chat(request, chat_id):
    chat = get_object_or_404(TogetherChat, id=chat_id)

    if not request.user in chat.user.all():
        return redirect("/")


    friends = Friend.objects.filter(user=request.user)

    if request.method == "POST":
        if 'add' in request.POST:
            add = request.POST.get("add")
            user_to_add = get_object_or_404(User, id=add)
            chat.user.add(user_to_add)


        return redirect("chat_view", chat_id=chat.id)

    return render(request, "add_user_in_chat.html", {"chat":chat, "friends":friends})


def list_user_in_togetherChat(request, chat_id):
    chat = get_object_or_404(TogetherChat, id=chat_id)

    if not request.user in chat.user.all():
        return redirect("/")

    list_user = chat.user.all()

    if request.method == "POST":
        if 'delete' in request.POST:
            delete = request.POST.get("delete")
            user_to_delete = get_object_or_404(User, id=delete)
            chat.user.remove(user_to_delete)

            return redirect("list_user_in_togetherChat", chat_id=chat.id)
        elif 'new_owner' in request.POST:
            new_owner = request.POST.get("new_owner")
            user_to_owner = get_object_or_404(User, id=new_owner)
            chat.owner = user_to_owner
            chat.save()

            return redirect("list_user_in_togetherChat", chat_id=chat.id)
        elif 'leave' in request.POST:
            user_to_leave = request.user
            all_user = chat.user.exclude(id=user_to_leave.id)

            if user_to_leave == chat.owner:

                if all_user.exists():
                    chat.owner = random.choice(list(all_user))
                    chat.save()

            chat.user.remove(user_to_leave)

            if not all_user.exists():
                chat.delete()
                    
            return redirect('profil_user')
                
    return render(request, "list_user_in_togetherChat.html", {"list_user":list_user, "chat":chat})