#coding=utf-8
import json

from django.conf import settings
from django.core.cache import cache

#from vmadmin.models import get_setting


CACHE_KEY_CEPH_LIST_ = 'CK_CEPH_LIST_%d'
CACHE_KEY_GROUP_ = 'CK_GROUP_%d'
CACHE_KEY_GROUP_LIST = 'CK_GROUP_LIST'
CACHE_KEY_IMAGE_LIST_ = 'CK_IAMGE_LIST_%d'
CACHE_KEY_IMAGE_LIST_BY_CEPHID_ = 'CK_IMAGE_LIST_CEPHID_%d'
CACHE_KEY_SESSION_ID = 'CK_SESSION_ID'
CACHE_KEY_VM_ = 'CK_VM_%s'
CACHE_KEY_VM_LIST_ = 'CK_VM_%d'

def get_cache(key):
    if settings.CACHE_ENABLE == False:
        return False
    
    res = cache.get(key, False)
    if not res == False:
#         print ('getcache', key, res)
        return json.loads(res)
    return False

def set_cache(key, value):
    if settings.CACHE_ENABLE == False:
        return 
    
    cache_time = get_cache_time()
#     print ('set cache', key, value, cache_time)
    cache.set(key, json.dumps(value), cache_time) 
    
def del_cache(key):
    if settings.CACHE_ENABLE == False:
        return 
    cache.set(key, '', -1)
    
def get_cache_time():
    from vmadmin.models import get_setting
    cache_time = get_setting(settings.SETTING_KEY_CACHE_EXP_TIME)
    if not cache_time:
        cache_time = settings.DEFAUTL_CACHE_EXP_TIME
    try:
        return int(cache_time)
    except:
        raise RuntimeError('settings DEFAULT_CACHE_EXP_TIME error.')

