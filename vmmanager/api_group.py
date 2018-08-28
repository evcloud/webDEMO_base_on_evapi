#coding=utf-8
from .api_auth import api_login
from .cache import get_cache, set_cache, CACHE_KEY_GROUP_, CACHE_KEY_GROUP_LIST
from .tools import *


@api_login
def api_get_group_list(session_id = None):
    '''获取集群列表'''
    group_list = get_cache(CACHE_KEY_GROUP_LIST)
    if group_list != False:
        return True, group_list
    url = '/api/v1/group/get_list/'
    args = {'session_id': session_id}
    data = do_post(url, args)
    if data:
        if data['res'] == True:
            set_cache(CACHE_KEY_GROUP_LIST, data['list'])
            return True, data['list']
        if 'err' in data:
            return False, data['err']
    return False, ''

@api_login    
def api_get_group(group_id, session_id = None):
    '''获取集群信息'''
    group = get_cache(CACHE_KEY_GROUP_ % int(group_id))
    if group != False:
        return True, group
    url = '/api/v1/group/get/'
    args = {'session_id': session_id, 'group_id': group_id}
    data = do_post(url, args)
    if data:
        if data['res'] == True:
            set_cache(CACHE_KEY_GROUP_ % int(group_id), data['info'])
            return True, data['info']
        if 'err' in data:
            return False, data['err']
    return False, ''