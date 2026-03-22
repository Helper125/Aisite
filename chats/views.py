from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from .forms import Register_login, ChatName, ProfilEdit
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .Ais import artificial_intelligence
import speech_recognition as sr
from gtts import gTTS
import os
from django.conf import settings
from django.http import FileResponse
from langdetect import *
from django.contrib.auth import get_user_model

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
    message = Message.objects.filter(chat=chat)

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
        

    return render(request, 'profil.html', {'profil':profil, "all_chats":all_chats})


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