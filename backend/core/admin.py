from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Jersey, PriceHistory, Like, Alert

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
    

class JerseyAdmin(admin.ModelAdmin):
    list_display = ('team', 'price', 'color', 'description') 

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Jersey, JerseyAdmin)
admin.site.register(PriceHistory)
admin.site.register(Like)
admin.site.register(Alert)

