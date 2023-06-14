from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_filter = ('username', 'email')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['password'].disabled = True
        return form


admin.site.site_title = 'Админка FOODGRAM'
admin.site.site_header = 'Администрирование сайта FOODGRAM'
