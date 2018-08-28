#coding=utf-8
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.utils import timezone

import json
from django.shortcuts import render, render_to_response

from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse

# from oauth import login_required
from django.contrib.auth.decorators import login_required
from .auth import interclient_user_required

from .models import VMUser


from django.views.decorators.http import require_http_methods
from random import choice
import string
from django.core.cache import cache
from message.models import Mail
import uuid
from django.contrib.auth.models import User 

@interclient_user_required
@login_required
def index(request):
    #return HttpResponseRedirect('/accounts/login/')
    if request.user.interclient_enable:
        return HttpResponseRedirect('/interclient/')
    return HttpResponseRedirect('/accounts/login/')

# @require_http_methods(['GET', 'POST'])
def register(request):
    info = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        res = True
        if not name or not email:
            res = False 
            info = '注册失败，请正确填写表单。'
        obj = VMUser()
        obj.email = email
        obj.name = name
        if obj.check_email():
            exist = VMUser.objects.filter(email = obj.email)
            u = User.objects.filter(email = obj.email)
            if u.exists() :
                res = False
                info = '用户已存在，请直接登陆。'
                if not exist.exists(): #登记没有注册记录的注册用户信息
                    obj.uuid = uuid.uuid4()
                    obj.regist_time = timezone.now() #datetime.now()
                    obj.confirm_time = timezone.now() #datetime.now()
                    obj.user = u[0]
                    obj.save()
            else:
                valid_date = timezone.now() + relativedelta(days = -7)
                # print(valid_date) 
                exist = exist.filter(regist_time__gt = valid_date)
                if exist:
                    exist[0].send_confirm_email(request.get_host())
                    res = False
                    info = '您已经注册,请登录邮箱进行验证,并设置密码'
                else:
                    obj.uuid = uuid.uuid4()
                    obj.confirm_time = None
                    obj.user = None
                    obj.save()
                    obj.send_confirm_email(request.get_host())
                    info = '请登录邮箱进行验证，并设置密码'
        else:
            info = '仅对 @cnic.cn 邮箱开放注册。'
        return HttpResponse(json.dumps({'res':res,'info':info}), content_type='application/json')
    else:
        return TemplateResponse(request,'accounts_register.html', {'info': info})
        #return render_to_response('accounts_register.html', {'info': info}, context_instance=RequestContext(request))

def confirm(request):
    user = None
    res  = True
    error = ''
    if request.method == "POST":
        uid = request.POST.get('uuid')
        passwd = request.POST.get('passwd')
        passwd2 = request.POST.get('passwd2')

        obj = VMUser.objects.filter(uuid = uid)
        if obj:
            user = obj[0]
            if user.is_confirmed():
                res = False
                error = '不能重复激活，请使用首次激活时设置的密码登录。'
        else:
            res = False
            error = 'UUID ERROR.'
        if res and len(passwd) < 6:
            res = False
            error = '密码长度不能小于6位。'
        if res and passwd != passwd2:
            res = False
            error = '两次输入密码不一致。'
        if res:
            uobj = User()
            uobj.username = user.email
            uobj.email = user.email
            #uobj.interclient_enable = True
            uobj.first_name = user.name
            uobj.set_password(passwd)
            uobj.vm_limit = user.default_vm_limit
            uobj.save()
            user.user = uobj
            user.confirm_time = timezone.now() #datetime.now()
            user.save()
            return HttpResponseRedirect('/accounts/')
        
    else:
        uid = request.GET.get('uuid')
        user = None
        if uid:
            obj = VMUser.objects.filter(uuid = uid)
            if obj:
                user = obj[0]
                if user.is_confirmed():
                    return HttpResponseRedirect('/interclient/')
    return TemplateResponse(request,'accounts_confirm.html',{'user': user, 'res': res, 'error': error})
    #return render_to_response('accounts_confirm.html', {'user': user, 'res': res, 'error': error}, context_instance=RequestContext(request))


@login_required
def passwd_reset(request):
    user = None
    res  = False
    resinfo = ''
    if request.method == "POST":
        passwd_old = request.POST.get('passwd_old')
        passwd = request.POST.get('passwd')
        passwd2 = request.POST.get('passwd2')
        obj = VMUser.objects.filter(user = request.user)
        if obj.exists():
            user = obj[0].user
            if user.check_password(passwd_old):
                res = True
            else:
                res = False
                resinfo = '原密码错误，请重新输入！'
        else:
                obj = VMUser()
                obj.uuid = uuid.uuid4()
                #obj.regist_time = datetime.now()
                #obj.confirm_time = datetime.now()
                obj.user = request.user
                obj.save()
                obj = VMUser.objects.filter(user = request.user)[0]
                obj.email = obj.user.email
                obj.name = obj.user.first_name
                obj.save()
                res = True
                user = request.user
        if res and len(passwd) < 6:
            res = False
            resinfo = '密码长度不能小于6位。'
        if res and passwd != passwd2:
            res = False
            resinfo = '两次输入密码不一致。'
        if res:
            user.set_password(passwd)
            user.save()
            resinfo = '修改成功，请重新登陆平台.'
        #if res == True:
        #    return HttpResponse("<script>alert('修改成功，请重新登陆平台.'); window.location.href='../login/';</script>")
    #return render_to_response('accounts_passwd_reset.html', {'user': user, 'res': res, 'resinfo': resinfo}, context_instance=RequestContext(request))
    return TemplateResponse(request,'accounts_passwd_reset.html',{'user': user, 'res': res, 'resinfo': resinfo})


def passwd_find(request):
    user = None
    res  = True
    error = ''
    resinfo=''
    if request.method == "POST":
        useremail = request.POST.get('email')
        obj = User.objects.filter(email = useremail)
        if obj.exists():
                exist = VMUser.objects.filter(user = obj[0])
                vmuser_obj = None
                if  exist.exists(): 
                    vmuser_obj = exist[0]
                else:                    #登记没有注册记录的注册用户信息
                    vmuser_obj = VMUser()
                    vmuser_obj.uuid = uuid.uuid4()
                    vmuser_obj.user = obj[0]
                    vmuser_obj.email = obj[0].email
                    vmuser_obj.name = obj[0].first_name
                    vmuser_obj.save()
                params={'domain':request.get_host(),'uuid':vmuser_obj.uuid,'subject':u'大数据部云主机平台账户密码找回'}
                res = _send_mail(useremail,'accounts_passwd_find_email.html',params)
                if res == True:
                    resinfo = '请登录邮箱，重置账号.'
        else:
            exist = VMUser.objects.filter(email = useremail)
            if exist.exists() and not exist[0].is_confirmed():
                res = False
                error = '账号还未激活，请先登陆邮箱激活账号。'
                #return HttpResponseRedirect('/accounts/')
            else:
                res = False
                error = '账号还未注册.'
    if res == False:
        resinfo = error
    #return render_to_response('accounts_passwd_find.html', {'resinfo':resinfo}, context_instance=RequestContext(request))
    return TemplateResponse(request,'accounts_passwd_find.html',{'resinfo':resinfo})



def _send_mail(user_email,template_name,params):
        mail = Mail()
        mail.receiver = user_email
        mail.subject = params['subject'] 
        from  django.template.loader  import  get_template 
        #from django.template import Context
        t = get_template(template_name)
        #mail.content = t.render(Context(params))
        mail.content = t.render(params)
        try:
            mail.save()
            mail.send()
            res = True
        except Exception as e:
            print (e)
            res = False
        return res


def passwd_find_confirm(request):
    user = None
    res  = False
    error = ''
    if request.method == "POST":
        uid = request.POST.get('uuid')
        passwd = request.POST.get('passwd')
        passwd2 = request.POST.get('passwd2')
        
        obj = VMUser.objects.filter(uuid = uid)
        if obj:
            if not obj[0].is_confirmed():
                res = False
                error = '账号还未激活，请先登陆邮箱激活账号。'
            else:
                user = obj[0].user
                res = True
        else:
            res = False
            error = '无法找回，请与管理员联系.'
        if res and len(passwd) < 6:
            res = False
            error = '密码长度不能小于6位。'
        else:
            res = True
        if res and passwd != passwd2:
            res = False
            error = '两次输入密码不一致。'
        else:
            res = True
        if res:
            user.set_password(passwd)
            user.save()
            return HttpResponseRedirect('/accounts/')
        
    else:
        uid = request.GET.get('uuid')
        user = None
        if uid:
            obj = VMUser.objects.filter(uuid = uid)
            if obj:
                user = obj[0]
                if user.is_confirmed():
                    res = True
                else:
                    res = False
                    error = '账户还未激活，请登录邮箱激活！'
    #return render_to_response('accounts_passwd_find_confirm.html', {'user': user, 'res': res, 'error': error}, context_instance=RequestContext(request))
    return TemplateResponse(request,'accounts_passwd_find_confirm.html',{'user': user, 'res': res, 'error': error})
