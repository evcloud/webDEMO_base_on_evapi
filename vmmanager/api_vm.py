#coding=utf-8
from .api_auth import api_login
from .cache import get_cache, set_cache, CACHE_KEY_VM_LIST_, CACHE_KEY_VM_
from .error import ERR_VM_UUID
from .tools import *


@api_login
def api_get_vm(vm_id, session_id = None):
    '''获取虚拟机信息'''
    vm_info = get_cache(CACHE_KEY_VM_ % str(vm_id))
    if not vm_info == False:
        return True, vm_info
    url = '/api/v1/vm/get/'
    args = {'session_id': session_id, 'uuid': vm_id}
    data = do_post(url, args)
    if data:
        if data['res'] == True:
            set_cache(CACHE_KEY_VM_ % str(vm_id), data['info'])
            return True, data['info']
        if 'err' in data:
            return False, data['err']
    return False, ''

@api_login
def api_get_vm_list(group_id, session_id = None):
    '''获取制定集群的虚拟机列表'''
    vm_list = get_cache(CACHE_KEY_VM_LIST_ % int(group_id))
    if not vm_list == False:
        return True, vm_list
    url = '/api/v1/vm/get_list/'
    args = {'session_id': session_id, 'group_id': group_id}
    data = do_post(url, args)
    if data:
        if data['res'] == True:
            set_cache(CACHE_KEY_VM_LIST_ % int(group_id), data['list'])
            return True, data['list']
        if 'err' in data:
            return False, data['err']
    return False, ''

@api_login        
def api_create_vm(group_id, image_id, net_type_id, vcpu, mem, remarks = '', session_id = None):
    '''创建虚拟机'''
    url = '/api/v1/vm/create/'
    args = {'session_id': session_id, 'group_id': group_id, 'image_id': image_id, 
            'net_type_id': net_type_id, 'vcpu': vcpu, 'mem': mem, 'remarks': remarks}

    data = do_post(url, args)
    if data:
        if data['res'] == True:
            return True, data['uuid']
        if 'err' in data:
            return False, data['err']
    return False, ''

@api_login
def api_get_vm_status(vm_id, session_id = None):
    '''获取制定虚拟机的状态'''
    url = '/api/v1/vm/status/'
    args = {'session_id': session_id, 'uuid': vm_id}
    data = do_post(url, args)
    if data:
        if data['res'] == True:
            return True, data['status']
        if 'err' in data:
            return False, data['err']
    return False, ''


def _api_vm_op(session_id, vm_id, op):
    '''发送虚拟机操作请求，外部逻辑不直接调用此函数'''
    url = '/api/v1/vm/op/'
    args = {'session_id': session_id, 'uuid': vm_id, 'op': op}
    data = do_post(url, args)
   
    if data:
        if data['res'] == True:
            return True, ''
        if 'err' in data:
            return False, data['err']
    return False, ''

@api_login
def api_start_vm(vm_id, session_id = None):
    '''启动虚拟机'''
    return _api_vm_op(session_id, vm_id, 'start')

@api_login
def api_reboot_vm(vm_id, session_id = None):
    '''重启虚拟机'''
    return _api_vm_op(session_id, vm_id, 'reboot')

@api_login
def api_shutdown_vm(vm_id, session_id = None):
    '''关闭虚拟机'''
    return _api_vm_op(session_id, vm_id, 'shutdown')

@api_login
def api_poweroff_vm(vm_id, session_id = None):
    '''关闭虚拟机电源'''
    return _api_vm_op(session_id, vm_id, 'poweroff')

@api_login
def api_delete_vm(vm_id, session_id = None):
    '''删除虚拟机'''
    res, info =  _api_vm_op(session_id, vm_id, 'delete')
    if res == False and info == ERR_VM_UUID:
        return True, ''
    return res, info

@api_login
def api_reset_vm(vm_id, session_id = None):
    '''重置虚拟机'''
    return _api_vm_op(session_id, vm_id, 'reset')

@api_login
def api_edit_vm_remarks(vm_id, remarks, session_id = None):
    '''修改虚拟机备注'''
    url = '/api/v1/vm/edit/'
    args = {'session_id': session_id, 'uuid': vm_id, 'remarks': remarks}
    data = do_post(url, args)
    if data:
        if data['res'] == True:
            return True, ''
        if 'err' in data:
            return False, data['err']
    return False, ''

@api_login
def api_edit_vm(vm_id, vcpu, mem, session_id = None):
    '''修改虚拟机配置'''
    url = '/api/v1/vm/edit/'
    args = {'session_id': session_id, 'uuid': vm_id, 'vcpu': vcpu, 'mem': mem}
    data = do_post(url, args)
    if data:
        if data['res'] == True:
            return True, ''
        if 'err' in data:
            return False, data['err']
    return False, ''