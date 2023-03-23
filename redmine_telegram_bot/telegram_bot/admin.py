from django.contrib import admin
from .models import Chat


class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


admin.site.register(Chat, ChatAdmin)
