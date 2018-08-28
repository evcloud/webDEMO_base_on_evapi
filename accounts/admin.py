from django.contrib import admin

# Register your models here.
from .models import VMUser

class VMUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'regist_time', 'confirm_time')
    list_filter = []
admin.site.register(VMUser, VMUserAdmin)