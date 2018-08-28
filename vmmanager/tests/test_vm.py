#coding=utf-8
from django.test import TestCase
from .. import api_auth_login

user = 'test'
passwd = 'cnic.cn'
net_type_id = 'local'


from .. import api_get_vm, api_get_vm_list, api_create_vm, api_get_vm_status, api_delete_vm

from .. import api_get_image_list
from .. import api_get_group_list
class VmTest(TestCase):
    def setUp(self):
        res, info = api_auth_login(user, passwd)
        if res:
            self.session_id = info
        
        res, info = api_get_group_list(self.session_id)
        if res:
            self.group_id = info[0]['id']
        else:
            self.group_id = None
        
        res, info = api_get_image_list(self.session_id, self.group_id)
        if res:
            self.image_id = info[0]['id']
        else:
            self.image_id = None
        self.vcpu = 2
        self.mem = 2048
        res, info = api_create_vm(self.session_id, self.group_id, self.image_id, net_type_id, self.vcpu, self.mem)
        if res:
            self.vm_id = info
        else:
            self.vm_id = None
    
    def tearDown(self):
        res, info = api_delete_vm(self.session_id, self.vm_id)
        
    
    def test_get_vm(self):
        res, info = api_get_vm(self.session_id, self.vm_id)
        self.assert_(res == True)
        if res:
            self.assertDictContainsSubset({'group_id': self.group_id, 'image_id': self.image_id,'vcpu': self.vcpu, 'mem':self.mem, 'uuid':self.vm_id}, info)
        
    def test_get_vm_list(self):
        res, info = api_get_vm_list(self.session_id, self.group_id)
        self.assert_(res == True)
        
    def test_create_vm(self):
        self.assert_(self.vm_id != None)
        
    def test_get_vm_status(self):
        res, info = api_get_vm_status(self.session_id, self.vm_id)
        self.assert_(res == True)
        self.assert_(info == 5)