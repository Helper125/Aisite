from django.contrib import admin
from .models import Chat, Message, Users

# Register your models here.

@admin.register(Chat)
class Chat(admin.ModelAdmin):
    pass

@admin.register(Message)
class Chat(admin.ModelAdmin):
    pass

@admin.register(Users)
class Chat(admin.ModelAdmin):
    pass