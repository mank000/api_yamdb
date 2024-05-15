# В алфавитном порядке?
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import YamdbUser


class YamdbUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'bio')}),
    )


admin.site.register(YamdbUser, YamdbUserAdmin)
