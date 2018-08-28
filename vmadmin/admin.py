#coding=utf-8
from django.contrib import admin
from .models import Vm, Tpl, Settings

class VmAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'group_id', 'vmid', 'deleted', 'cpu', 'mem', 'image', 'start_time', 'end_time')
    list_filter = ['user', 'group_id', 'deleted', 'image']
admin.site.register(Vm, VmAdmin)

class TplAdmin(admin.ModelAdmin):
    list_display = ('cpu', 'mem', 'term')
admin.site.register(Tpl, TplAdmin)
    
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'desc')
admin.site.register(Settings, SettingsAdmin)    
