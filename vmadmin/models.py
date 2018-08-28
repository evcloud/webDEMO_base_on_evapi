#coding=utf-8
from django.contrib.auth.models import User 
from django.db import models

class Vm(models.Model):
    user = models.ForeignKey(User)
    group_id = models.IntegerField()
    vmid     = models.CharField(max_length=100, unique=True)
    deleted  = models.BooleanField(default=False)
    cpu      = models.IntegerField()
    mem      = models.IntegerField()
    image    = models.CharField(max_length=200)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    remarks = models.TextField(null=True, blank=True)
    ipv4 = models.GenericIPAddressField()

    class Meta:
        verbose_name = '虚拟机'
        verbose_name_plural = verbose_name
        


class Tpl(models.Model):
    cpu = models.IntegerField('cpu数', help_text='个')
    mem = models.IntegerField('内存大小', help_text='MB')
    term = models.IntegerField('有效期', help_text='月')

    class Meta:
        verbose_name = '虚拟机性能参数'
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return u"%d个CPU | %dMB内存 | %d个月有效期" %(self.cpu, self.mem/1024, self.term)

class Settings(models.Model):
    key = models.CharField(primary_key=True, max_length=100)
    value = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = '系统设置'
        verbose_name_plural = verbose_name

def get_setting(key):
    setting = Settings.objects.filter(key = key)
    if setting:
        return setting[0].value
    return ''