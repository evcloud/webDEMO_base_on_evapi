#coding=utf-8

##########################################################
# @author： bobfu
# @email: fubo@cnic.cn
# @date: 2015-11-18 
# @desc: 对vmmanger系统的web api进行封装
##########################################################
from .api_auth import api_auth_login, api_auth_logout
from .api_ceph import api_get_ceph_list
from .api_group import api_get_group_list, api_get_group
from .api_image import api_get_image_list
from .api_vm import (api_get_vm, api_get_vm_list, api_create_vm, api_get_vm_status, 
                     api_start_vm, api_reboot_vm, api_shutdown_vm, api_poweroff_vm, 
                     api_delete_vm, api_reset_vm, api_edit_vm_remarks, api_edit_vm) 
from .api_vnc import api_get_vnc_url