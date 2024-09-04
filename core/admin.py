from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Jersey, PriceHistory, Like, Alert


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Jersey)
admin.site.register(PriceHistory)
admin.site.register(Like)
admin.site.register(Alert)