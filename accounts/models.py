#coding=utf-8
from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import User 
from datetime import datetime
from django.utils import timezone
from message.models import Mail
from django.contrib.auth.admin import UserAdmin

class VMUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    regist_time = models.DateTimeField(auto_now_add=True)
    confirm_time = models.DateTimeField(null=True, blank=True)
    uuid = models.CharField(max_length=100)
    user = models.OneToOneField(User, null=True, blank=True)

    class Meta:
        verbose_name = '用户注册记录'
        verbose_name_plural = verbose_name
        
    def check_email(self):
        if self.email == 'lzxddz@qq.com': #测试使用
            return True
        if self.email[-8:] == '@cnic.cn':
            return True
        return False

    def is_confirmed(self):
        if self.user == None:
            return False
        return True

    def send_confirm_email(self, domain):
        mail = Mail()
        mail.receiver = self.email
        mail.subject = u'大数据部云主机平台账户注册-账户激活'
        from  django.template.loader  import  get_template 
        from django.template import Context
        #t = get_template('interclient_regist_confirm.html')
        t = get_template('accounts_regist_confirm.html')
        #mail.content = t.render(Context({'domain':domain, 'uuid':self.uuid, 'subject': mail.subject})) #1.8以上版本此用法被废弃
        mail.content = t.render({'domain':domain, 'uuid':self.uuid, 'subject': mail.subject})
        try:
            mail.save()
            mail.send()
            res = True
        except Exception as e:
            res = False

    def confirm(self):
        if not self.is_confirmed() and self.check_email() and not User.objects.filter(username=self.email).exists():
            obj = User()
            obj.username = self.email
            obj.interclient_enable = True
            obj.email = self.email
            obj.save()
            self.confirm_time = timezone.now()#datetime.now()
            self.save()
            return True
        return False
    
    @property
    def default_vm_limit(self):
        from vmadmin.models import get_setting
        limit = get_setting(settings.SETTING_KEY_DEFAULT_VM_LIMIT)
        if limit:
            return limit
        return settings.DEFAULT_VM_LIMIT
        
class ProfileBase(type):                    
    def __new__(cls,name,bases,attrs):      
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]  
        if parents:  
            fields = []  
            for obj_name, obj in attrs.items():  
                if isinstance(obj, models.Field): fields.append(obj_name)  
                User.add_to_class(obj_name, obj)  
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)  
            UserAdmin.fieldsets.insert(1, (name, {'fields': fields}))  
            UserAdmin.list_display = tuple(list(UserAdmin.list_display) + fields)
            UserAdmin.list_display = tuple(list(UserAdmin.list_display) + ['is_superuser'])
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)  

class ProfileUser(object,metaclass=ProfileBase):  
    pass  
    
class MyProfile(ProfileUser):  
    vm_limit = models.IntegerField('虚拟机数限制', default=settings.DEFAULT_VM_LIMIT)
UserAdmin.list_filter = tuple(list(UserAdmin.list_filter) + ['vm_limit'])
