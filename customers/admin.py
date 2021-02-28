from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Customer,UserAccessGroup


class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ('id', 'email','phone','code','is_active',)
    list_filter = ('email','is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('first_name','last_name','phone','code',)}),
        ('Permissions', {'fields': ('is_active',)}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_active',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(UserAccessGroup)
class UserAccessGroupAdmin(admin.ModelAdmin):
    list_display=("id","user","group",)

admin.site.register(Customer, CustomerAdmin)
