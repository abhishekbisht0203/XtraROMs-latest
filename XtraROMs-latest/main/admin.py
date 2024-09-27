from django.contrib import admin
from .models import *

# Register your models here.
class CustomROMAdmin(admin.ModelAdmin):
    filter_horizontal = ('device',)
    list_display = ('name', 'credits', 'upload_date')
    search_fields = ('name', 'credits')
admin.site.register(CustomROM, CustomROMAdmin)

class CustomMODAdmin(admin.ModelAdmin):
    list_display = ('name', 'credits', 'upload_date')
    search_fields = ('name', 'credits')
admin.site.register(CustomMOD, CustomMODAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_authorized')
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(ROMLike)

admin.site.register(MODLike)

admin.site.register(Credits)

admin.site.register(Comment)

admin.site.register(Blog)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'codename')
admin.site.register(Device, DeviceAdmin)