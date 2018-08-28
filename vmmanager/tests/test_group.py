#coding=utf-8
from django.test import TestCase
from .. import api_auth_login

user = 'test'
passwd = 'cnic.cn'
group_id = 1

from .. import api_get_group_list, api_get_group
class GroupTest(TestCase):
    def setUp(self):
        res, info = api_auth_login(user, passwd)
        if res:
            self.session_id = info
         
    
    def test_get_group_list(self):
        res, info = api_get_group_list(self.session_id)
        self.assert_(res == True)
    
    def test_get_group(self):
        res, info = api_get_group(self.session_id, group_id)
        self.assert_(res == True)
        