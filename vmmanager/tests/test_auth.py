#coding=utf-8
from django.test import TestCase
from .. import api_auth_login

user = 'test'
passwd = 'cnic.cn'

class AuthTest(TestCase):
    def setUp(self):
        self.apiuser = 'test'
        self.apipasswd = 'cnic.cn'
        self.apihost = 'vm.cnic.cn'
        
    def test_login(self):
        res = api_auth_login(self.apiuser, self.apipasswd)
        print (res)
        