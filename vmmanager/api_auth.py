#coding=utf-8
import time

from django.conf import settings

from .cache import get_cache_time, get_cache, set_cache, CACHE_KEY_SESSION_ID, del_cache
from .error import ERR_AUTH_NO_LOGIN
from .tools import *


def api_auth_login(api_user = settings.VMMANAGER_USER, api_passwd = settings.VMMANAGER_PASSWORD):
    '''api访问:获取session_id'''
    urllogin='/api/v1/auth/login/'
    paramlogin= {'login_name':api_user,'password':api_passwd, 'expiry': get_cache_time() + 30}
    data = do_post(urllogin, paramlogin)
    if data:
        if data['res'] == True:
            set_cache(CACHE_KEY_SESSION_ID, data['session_id'])
            return True, data['session_id']
        if 'err' in data:
            return False, data['err']
    return False, ''

def get_session_id():
    session_id = get_cache(CACHE_KEY_SESSION_ID)
    if session_id != False:
        return session_id
    res, session_id = api_auth_login()
    if res:
        return session_id
    
def api_auth_logout():
    '''注销'''
    urllogout='/api/v1/auth/logout/'
    data = do_post(urllogout)
    if data:
        if data['res'] == True:
            del_cache(CACHE_KEY_SESSION_ID)
            return True, ''
        if 'err' in data:
            return False, data['err']
    return False, ''

#################################
def api_login(func):
    def handle_args(*args, **kwargs): 
        try:
#             start_time = time.time()
            
            session_id = get_session_id()
            kwargs['session_id'] = session_id
#             print(session_id, args, kwargs, func) 
            res, err = func(*args, **kwargs)
            if res == False and err == ERR_AUTH_NO_LOGIN:
                login_res, session_id = api_auth_login()
                #print ("api_login",login_res, session_id)
                if login_res:
                    kwargs['session_id'] = session_id
                    res, err = func(*args, **kwargs)
            
#             end_time = time.time()
#             print (func.__module__, func.__name__, ' process time: ', end_time - start_time)
            return res, err
        except Exception as e:
            return False, ''
    handle_args.__name__ = func.__name__
    handle_args.__module__ = func.__module__
    return handle_args