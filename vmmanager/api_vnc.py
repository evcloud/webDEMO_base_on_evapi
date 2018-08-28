#coding=utf-8
from .api_auth import api_login
from .tools import *


@api_login
def api_get_vnc_url(vm_id, session_id = None):
    url = '/api/v1/vnc/open/'
    args = {'session_id': session_id, 'uuid': vm_id}
    data = do_post(url, args)
    if data:
        if data['res'] == True:
            return True, data['url']
        if 'err' in data:
            return False, data['err']
    return False, ''