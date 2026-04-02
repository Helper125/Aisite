from django.contrib import admin
from .models import Chat, Message, Users, FriendRequest, Friend, TogetherChat, MessageInChat

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

@admin.register(FriendRequest)
class Chat(admin.ModelAdmin):
    pass

@admin.register(Friend)
class Chat(admin.ModelAdmin):
    pass

@admin.register(TogetherChat)
class Chat(admin.ModelAdmin):
    pass

@admin.register(MessageInChat)
class Chat(admin.ModelAdmin):
    pass