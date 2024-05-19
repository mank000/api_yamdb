from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import YamdbUser


class YamdbUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'bio')}),
    )

    list_display = ('username', 'email',
                    'first_name', 'last_name', 'role', 'is_staff')

    list_editable = ('role',)

    list_display_links = ('username', 'email')


admin.site.register(YamdbUser, YamdbUserAdmin)
