from django.contrib import admin
from .models import Chat


class RedmineGroupInline(admin.TabularInline):
    model = Chat.groups.through

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj=obj)


class TaskInline(admin.TabularInline):
    model = Chat.tasks.through

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj=obj)


class ChatAdmin(admin.ModelAdmin):
    inlines = [RedmineGroupInline, TaskInline]
    list_display = ('name', 'is_active')
    readonly_fields = ['chat_id', ]


admin.site.register(Chat, ChatAdmin)
