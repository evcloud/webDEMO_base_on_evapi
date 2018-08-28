#coding=utf-8
from django.utils import timezone
import json
from random import choice
import string
import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .auth import interclient_user_required
from dateutil.relativedelta import relativedelta
from message.models import Mail
from vmadmin.vmadmin import VmAdmin 


vmadmin1 = VmAdmin()

@login_required
def index(request):
    return HttpResponseRedirect('/interclient/vm/list/')
#    if request.user.interclient_enable:
#        return HttpResponseRedirect('/interclient/vm/list/')
#    return HttpResponseRedirect('/accounts/login/')



@login_required
def vm_list(request):
    dic = {}
    r=vmadmin1.vmlist(request.user)
    vms=[]
    if r['res']:
        for v in r['list']:
            vm={}
            vm['user']=request.user
            #vm['username']=v['username']
            #vm['deleted']=v['deleted']
            vm['vmid']=v['vmid']
            vm['uuid']=v['uuid']
            vm['cpu']=v['cpu']
            vm['mem']=v['mem']
            vm['image']=v['image']
            vm['ipv4']=v['ipv4']
            vm['start_time']=v['start_time']
            vm['end_time']=v['end_time']
            vm['remarks']=v['remarks']
            vm['expired']=False
            if vm['end_time'] != None and vm['end_time']<timezone.now() :
                vm['expired']=True
            vms.append(vm)
    dic['vms'] = vms
    return TemplateResponse(request,'interclient_list.html', dic)

@login_required
def vm_create(request):
    dic = {}
    r=vmadmin1.vm_can_create(request.user)
    if r['res'] == False:
        dic['cant_create'] = True
        dic['error'] = r['error']
        return TemplateResponse(request,'interclient_create.html', dic) 
    if request.method == 'POST':
        group = request.POST.get('group')
        image = request.POST.get('image')
        tpl = request.POST.get('tpl')
        if image and group and tpl:
            r=vmadmin1.vmcreate(request.user,group,image,tpl)
            if r['res'] == True:
                return HttpResponseRedirect('/interclient/vm/list/')
            else:
                dic['error'] = r['error']
        else:
                dic['error'] = 'error'
    r=vmadmin1.grouplist(request.user)
    groups=[]
    if r['res'] == True:
        for g in r['list']:
            groups.append({'group_id':g['id'],'name':g['name'],'desc':g['desc']})
    dic['groups'] = groups

    arg_group = request.GET.get('group')    
    if not arg_group and len(groups) > 0:
        arg_group = groups[0]['group_id']
    if arg_group:
        #��ȡ�����б�
        
        r=vmadmin1.imagelist(request.user,arg_group)
        images=[]
        if r['res'] == True:
            for i in r['list']:
                fullname='%s %s' %(i['name'], i['version'])
                images.append({'image_id':i['image_id'],'name':i['name'],'fullname':fullname,'version':i['version'],'type':i['type']})
        dic['images'] = images
        dic['type_images'] = {}
        for image in dic['images']:
            if image['type'] in dic['type_images']:
                dic['type_images'][image['type']].append(image)
            else:
                dic['type_images'][image['type']] = [image]
        tpls=[]  
        r=vmadmin1.tpllist(request.user)  #�˴����޸�
        if r['res'] == True:
            for t in r['list']:
                text1="%d vcpu | %d MB mem | %d month(s)" %(t['cpu'], t['mem'], t['term'])
                tpls.append({'tpl_id':t['tpl_id'],'cpu':t['cpu'],'mem':t['mem'],'term':t['term'],'text':text1})
        dic['tpls'] = tpls
    return TemplateResponse(request,'interclient_create.html', dic)

@login_required
def vm_edit_remarks(request):
    if request.method == 'POST':
        vmid = request.POST.get('vmid')
        remarks = request.POST.get('remarks')
    r=vmadmin1.edit_remarks(request.user,vmid,remarks)
    if r['res'] == True:
        return HttpResponse(json.dumps({'res': True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'res': False}), content_type='application/json')

@login_required
def vm_detail(request):
    dicts = {}
    vmid = request.GET.get('vmid')
    r = vmadmin1.vmdetail(request.user,vmid)
    if r['res'] == True:
        vminfo = r['vminfo']
        vmobj={}
        vmobj['name']=vminfo['name']
        vmobj['uuid']=vminfo['vmid']
        vmobj['vcpu']=vminfo['vcpu']
        vmobj['mem']=vminfo['mem']
        vmobj['image']=vminfo['image']
        vmobj['state']=vminfo['state']
        vmobj['vcpus']=vminfo['vcpus']
        vmobj['maxmem']=vminfo['maxmem']
        dicts['vmobj']=vmobj
    #dicts.update(VmAction(vmid).get_detail())
    return TemplateResponse(request,'interclient_detail.html', dicts)
    #return render_to_response('interclient_detail.html', dicts, context_instance=RequestContext(request))

@login_required
def vm_novnc(request):
    #vncid = request.GET.get("vncid")
    #if vncid:
    #    del_vnc_token(request.user,vncid)
    #    return HttpResponse('<script language="javascript">window.close();</script>')
    #else:
    vmid = request.GET.get('vmid')
    r = vmadmin1.set_vnc_token(request.user,vmid)
    if r['res'] == True:
        info = r['info']
        #return render_to_response('novnc.html', info, context_instance=RequestContext(request))
        url_str = info['url']
        url_str = url_str.replace(settings.VMMANAGER_HOST,settings.VNC_HOST)
        return HttpResponseRedirect(url_str)
    return HttpResponse('vnc not available.')

@login_required
def vm_status( request):
    if request.method == 'POST':
        vmid = request.POST.get('vmid')
        r = vmadmin1.vmstatus(request.user,vmid)
        if r['res'] == True:
            return HttpResponse(json.dumps({'res': True,'vmid': vmid, 'status': r['state']}), content_type='application/json') 
        else:
            return HttpResponse(json.dumps({'res': False, 'error':r['error']}), content_type='application/json') 
    return HttpResponse(json.dumps({'res': False}), content_type='application/json') 

@login_required
def vm_action( request):
    if request.method == 'POST':
        vmid   = request.POST.get('vmid')
        action = request.POST.get('op')
        r = vmadmin1.vmaction(request.user,vmid,action)
        return HttpResponse(json.dumps({'res': r['res']}), content_type='application/json') 
    return HttpResponse(json.dumps({'res': res}), content_type='application/json') 
