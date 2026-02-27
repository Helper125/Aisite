from django.shortcuts import render, redirect
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from .forms import Register_login
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .Ais import artificial_intelligence
import speech_recognition as sr
from gtts import gTTS
import os
from django.conf import settings
from django.http import FileResponse
from langdetect import *


# Create your views here.

@login_required
def chats(request):
    chat, _ = Chat.objects.get_or_create(user=request.user)
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

        

        return redirect("/")

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

        return redirect("/")


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
