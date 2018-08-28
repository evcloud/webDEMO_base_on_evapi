from django.conf.urls import include, url
from .views import  index,vm_create,vm_list,vm_detail,vm_novnc,vm_action,vm_status,vm_edit_remarks
#from topo import topo
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', index),
    url(r'^login/$',  login, {'template_name':'accounts_login.html'}), 
    url(r'^logout/$', logout),
    url(r'^vm/create/$',vm_create),
    url(r'^vm/list/$',vm_list),
    url(r'^vm/detail/$',vm_detail),
    url(r'^vm/novnc/$',vm_novnc),
    url(r'^vm/action/$',vm_action),
    url(r'^vm/status/$',vm_status),
    url(r'^vm/edit_remarks/$',vm_edit_remarks),
]
