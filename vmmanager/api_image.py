#coding=utf-8
from .api_auth import api_login
from .api_ceph import api_get_ceph_list
from .cache import get_cache, set_cache, CACHE_KEY_IMAGE_LIST_, CACHE_KEY_IMAGE_LIST_BY_CEPHID_
from .tools import *


@api_login
def api_get_image_list(group_id, session_id = None):
    '''获取某个集群的镜像列表'''
    image_list = get_cache(CACHE_KEY_IMAGE_LIST_ % int(group_id))
    if image_list != False:
        return True, image_list
    #根据group_id获取ceph_list
    res, info = api_get_ceph_list(group_id, session_id = session_id)
    if not res:
        return False, info
    ceph_list = info
    
    #根据ceph_list， 以ceph_id获取image——list
    image_list = []
    for ceph in ceph_list:
        images = _api_get_image_list_by_ceph_id(session_id, ceph['id'])
        image_list += images
    set_cache(CACHE_KEY_IMAGE_LIST_ % int(group_id), image_list)
    return True, image_list


def _api_get_image_list_by_ceph_id(session_id, ceph_id):
    '''获取制定ceph节点的镜像列表， 当做工具函数，对上层逻辑透明'''
    image_list = get_cache(CACHE_KEY_IMAGE_LIST_BY_CEPHID_ % int(ceph_id))
    if image_list != False:
        return image_list
    url = '/api/v1/image/get_list/'
    args = {'session_id': session_id, 'ceph_id': ceph_id}
    data = do_post(url, args)
    if data and data['res']:
        set_cache(CACHE_KEY_IMAGE_LIST_BY_CEPHID_ % int(ceph_id), data['list'])
        return data['list']
    return []
    