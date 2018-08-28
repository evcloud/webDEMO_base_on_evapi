#coding=utf-8
from datetime import datetime
from django.utils import timezone

from django.conf import settings

from dateutil.relativedelta import relativedelta
from .models import Vm, Tpl, get_setting
from vmmanager import api_auth, api_group, api_image, api_vm, api_vnc



class VmAdmin(object):
    def vmlist(self,user):
        vms=Vm.objects.filter(user = user,deleted = False)
        lists=[]
        for v in vms:
            if v.deleted == True:
                continue
            vminfo={}
            vminfo['user'] = user
            vminfo['vmid'] = v.vmid
            vminfo['uuid'] = v.vmid
            vminfo['cpu'] = v.cpu #rinfo['vcpu']
            vminfo['mem'] = v.mem #rinfo['mem']
            vminfo['image'] = v.image #rinfo['image']
            vminfo['start_time'] = v.start_time
            vminfo['end_time'] = v.end_time
            vminfo['ipv4'] = v.ipv4
            vminfo['remarks'] = v.remarks
            lists.append(vminfo)
        return {'res':True,'list':lists}
    
    

    #判断用户虚拟机数量是否超过系统限制
    def vm_can_create(self,user):
        result = {}
        vm_num = Vm.objects.filter(user = user, deleted=False).count()
        if vm_num < user.vm_limit:
            result = {'res':True}
        else:
            result = {'res':False,'error':'虚拟机数量超出限制'}
        return result
    
    
    #创建虚拟机
    def vmcreate(self,user,group_id,image_id,tpl):
        result = {}
        if self.vm_can_create(user) == False:
            result['res'] = False
            result['error'] = '云主机数量达到上限，您不能再创建新的云主机。'
        else:
            nettype = self._get_net_type_code()
            tpl = Tpl.objects.get(pk=tpl)
            vcpu = int(tpl.cpu)
            mem = int(tpl.mem)
            
            try:
                group_id = int(group_id)
                image_id = int(image_id)
            except: 
                result['res'] = False
                result['error'] = '参数有误'
            else:
                vm_created = False
                group_ok = False
                image_ok = False
                
                group_ok, group_info = api_group.api_get_group(group_id)
                if group_ok:
                    image_list_found, image_list = api_image.api_get_image_list(group_id)
                    if image_list_found:
                        for i_info in image_list:
                            if i_info['id'] == image_id:
                                image_info = i_info
                                image_ok = True
                                break
                
                if image_ok and group_ok:
                    vm_created, vmid = api_vm.api_create_vm(group_id, image_id, nettype, vcpu, mem, user.username)
                
                if vm_created:
                    now = timezone.now()#datetime.now()
                    obj = Vm()
                    obj.user = user
                    obj.group_id = group_id
                    obj.vmid = vmid
                    obj.cpu = vcpu
                    obj.mem = mem
                    obj.image = image_info['name'] + ' ' + image_info['version']
                    obj.start_time = now
                    obj.end_time = now + relativedelta(months=tpl.term)
                    res1,res2 = api_vm.api_get_vm(vmid)
                    if res1 == True:
                        obj.ipv4 = res2['ipv4']
                    else:
                        obj.ipv4 = ''
                    obj.save()
                    result['res'] = True
                    result['list'] = []
                else:
                    result['res'] = False
                    result['error'] = 'fail !'
 
        return result
    
    def vmdetail(self,user,vmid):
        result = {}
        v = Vm.objects.filter(user = user,vmid = vmid)
        if v.count() == 0:
            result = {'res':False , 'error':'vm not exist!'}
            return result
        res,sessionid = api_auth.api_auth_login()
        if res != True:
            result = {'res':False,'error':'fail to access api'}
            return result
        res,info = api_vm.api_get_vm(vmid,sessionid )
        if res != True:
            result = {'res':False,'error':info}
        else:
            vminfo={}
            vminfo['name'] = info['name']
            vminfo['vmid'] = info['uuid']
            vminfo['image']= info['image']
            vminfo['vcpu'] = info['vcpu']
            vminfo['mem']  = info['mem']
            vminfo['vcpus']= info['vcpu']
            vminfo['vcpus'] = info['vcpu']
            vminfo['maxmem'] = info['mem']
            r = self.vmstatus(user,vmid) 
            if r['res'] == True:
                vminfo['state'] = r['state']
            else:
                vminfo['state'] = 'NULL'
            result = {'res':res,'vminfo':vminfo}
        return result
    
    #修改remarks
    def edit_remarks(self,user,vmid,remarks):
        result = {}
        v=Vm.objects.filter(user = user,vmid = vmid)
        if v :
            try:
                v = v[0]
                v.remarks = remarks
                v.save()
                result['res']=True
            except Exception as e:
                result['res'] = False
                result['error'] = '无法修改'
        else:
            result['res'] = False
            result['error'] = '无虚拟机信息'
        return result


    def vmstatus(self,user,vmid):
        vm = Vm.objects.filter(user = user, vmid = vmid)
        if vm.exists():
            vm = vm[0]
        else:
            return {'res': False, 'error': '权限错误'}
        
        res, info = api_vm.api_get_vm_status(vmid)
        if res:
            return {'res': True, 'state': info}
       
        return {'res': False, 'error': '获取状态失败'}
    
    
    #action:'start'启动 'shutdown':关机 'reboot':重启 'poweroff':关闭电源 delete:'删除'
    #执行之后的状态：'running' 'shut off' 'running' 'shut off' 
    def vmaction(self,user,vmid,action):
        vm = Vm.objects.filter(user = user, vmid = vmid)
        if vm.exists():
            vm = vm[0]
        else:
            return {'res': False, 'error': '权限错误'}
        
        func_map = {
            'start': api_vm.api_start_vm,
            'shutdown': api_vm.api_shutdown_vm,
            'reboot': api_vm.api_reboot_vm,
            'poweroff': api_vm.api_poweroff_vm,
            'delete': api_vm.api_delete_vm
        }
        if action in func_map.keys():
            res, info = func_map[action](vmid)
            if res:
                if action == 'delete':
                    vm.deleted = True
                    vm.save()
                return {'res': True, 'status': 5}
            
            return {'res': False, 'error': '操作失败'}
        return {'res': False, 'error': '指令错误'}
    
    
    
    def set_vnc_token(self,user,vmid):
        result = {}
        v=Vm.objects.filter(user = user,vmid = vmid)
        if v:
            res1,res2 = api_vnc.api_get_vnc_url(vmid)
            if res1 == True:
                vncurl = res2
                result = {'res':True,'info':{'url':vncurl}}
            else:
                result = {'res':False,'error':'vnc not available!'}
        else:
            result = {'res':False,'error':'fail to access api'}
        return result

    
    
    def grouplist(self,user):
        result={}
        groups = []
        res1,res2 = api_group.api_get_group_list()
        if res1 == True:
            for g in res2:
                groups.append({'id':g['id'],'name':g['name'],'desc':g['desc']})
            result = {'res':True,'list':groups}
        else:
            result = {'res':False,'error':res2}
        return result
    
    
    def imagelist(self,user,group_id):
        result={}
        images = [] 
        res1,res2 = api_image.api_get_image_list(group_id)
        if res1 == True:
            for i in res2:
                images.append({'image_id':i['id'],'name':i['name'],'version':i['version'],'type':i['type']})
            result = {'res':True,'list':images}
        else:
            result = {'res':False,'error':res2}
        return result

    
    def tpllist(self,user):
        result = {}
        tpls = []
        tplall = Tpl.objects.all()
        for t in tplall:
            tpls.append({'tpl_id':t.id,'cpu':t.cpu,'mem':t.mem,'term':t.term})
        result = {'res':True,'list':tpls}
        return result
    
    def nettypelist(self,user):
        res=True
        error=''
        lists=[]
        result={}
        lists.append({
                 'type':'local',
                 'type_name':'内网'})
        if res:
            result = {'res':res,'list':lists}
        else:
            result = {'res':res,'error':error}
        return result
    
    def _get_net_type_code(self):
        code = get_setting(settings.SETTING_KEY_LOCAL_NET_CODE)
        if not code:
            return settings.DEFAULT_LOCAL_NET_CODE
        return code
