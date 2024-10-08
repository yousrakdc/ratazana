from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Jersey, PriceHistory, Like, Alert, JerseyImage

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
    

class JerseyImageInline(admin.TabularInline):
    model = JerseyImage
    extra = 1  # Allows to add multiple images in one go

class JerseyAdmin(admin.ModelAdmin):
    list_display = ('brand', 'team', 'price', 'season', 'is_promoted', 'is_upcoming', 'is_new_release')
    search_fields = ('brand', 'team')
    list_filter = ('is_promoted', 'is_upcoming', 'is_new_release')
    inlines = [JerseyImageInline]  # Add the inline for images
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Jersey, JerseyAdmin)
admin.site.register(PriceHistory)
admin.site.register(Like)
admin.site.register(Alert)

