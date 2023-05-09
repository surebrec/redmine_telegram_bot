from django.contrib import admin
from .models import RedmineGroup, RedmineUser


class RedmineGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_valid']
    readonly_fields = ['name', 'is_valid']

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.is_valid:
            return False
        return super().has_change_permission(request, obj=obj)


admin.site.register(RedmineGroup, RedmineGroupAdmin)


class RedmineUserAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'group']


admin.site.register(RedmineUser, RedmineUserAdmin)
