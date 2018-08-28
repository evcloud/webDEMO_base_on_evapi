#coding=utf-8
from .api_auth import api_login
from .api_group import api_get_group
from .cache import get_cache, set_cache, CACHE_KEY_CEPH_LIST_
from .tools import *

@api_login
def api_get_ceph_list(group_id, session_id = None):
    #根据group_id 获取center_id
    ceph_list = get_cache(CACHE_KEY_CEPH_LIST_ % int(group_id))
    if ceph_list != False:
        return True, ceph_list
    res, info = api_get_group(group_id, session_id = session_id)
    if res == False:
        return False, info
    group = info 
    center_id = group['center_id']

    #根据center_id获取ceph_list
    url = '/api/v1/ceph/get_list/'
    args = {'session_id': session_id, 'center_id': center_id}
    data = do_post(url, args)
    
    if data:
        if data['res'] == True:
            set_cache(CACHE_KEY_CEPH_LIST_ % int(group_id), data['list'])
            return True, data['list']
        if data.has_key('err'):
            return False, data['err']
    return False, ''