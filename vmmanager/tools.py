#coding=utf-8
import time
import urllib, http.client, json

from django.conf import settings


api_host = settings.VMMANAGER_HOST
api_version = 'v1'

def do_post(url, args = {}):
    '''发送post请求'''
    start_time = time.time()
    args = urllib.parse.urlencode(args) 
    headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}
    conn = http.client.HTTPConnection(api_host)
    conn.request('POST',url, args, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = json.loads(res.read())
        end_time = time.time()
        #print ('request time:', end_time - start_time, url)
        return data
    return False





    