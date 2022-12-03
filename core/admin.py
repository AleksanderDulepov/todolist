from django.contrib import admin
from django.contrib.auth.password_validation import validate_password

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')

    # для возможности изменения пароля из админки
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            new_password = form.data['password']
            # проверка валидности пароля
            validate_password(new_password)
            obj.set_password(new_password)
            obj.save()
        super(UserAdmin, self).save_model(request, obj, form, change)
