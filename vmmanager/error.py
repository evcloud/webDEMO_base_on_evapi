#coding=utf-8

ERR_AUTH_NO_LOGIN       = '40001'
ERR_AUTH_LOGIN          = '40002'
ERR_AUTH_LOGOUT         = '40003'
ERR_AUTH_PERM           = '40004'
ERR_GROUP_ID            = '40005'
ERR_HOST_ID             = '40006'
ERR_IMAGE_ID            = '40007'
ERR_CEPH_ID             = '40008'
ERR_VLAN_ID             = '40009'
ERR_VM_UUID             = '40010'
ERR_VM_NO_OP            = '40011'
ERR_ARGS_VM_VCPU        = '40012'
ERR_ARGS_VM_MEM         = '40013'
ERR_ARGS_VM_EDIT_NONE   = '40014'
ERR_ARGS_REQUIRED       = '40015'

ERR_ARGS_DECORATOR      = '50001'
ERR_PROCESS             = '50002'
ERR_LOG                 = '50003'
ERR_VLAN_NO_FIND        = '50004'
ERR_VM_DEFINE           = '50005'
ERR_VM_OP               = '50006'
ERR_VM_EDIT_REMARKS     = '50007'
ERR_VM_EDIT             = '50008'
ERR_VM_MIGRATE          = '50009'

STRERR_EN = {
    ERR_ARGS_DECORATOR:     'decorator args_required can not used here.',
    ERR_ARGS_REQUIRED:    'args not exists.',
    ERR_PROCESS:            'processing error.',
    ERR_LOG:                'log error.',
    ERR_AUTH_NO_LOGIN:      'user not login.',
    ERR_AUTH_LOGIN:         'login error.',
    ERR_AUTH_LOGOUT:        'logout error.',
    ERR_AUTH_PERM:          'permission error.',
    ERR_GROUP_ID:           'group id error.',
    ERR_HOST_ID:            'host id error.',
    ERR_IMAGE_ID:           'image id error.',
    ERR_CEPH_ID:            'ceph id error.',
    ERR_VLAN_NO_FIND:       'vlan not find.',
    ERR_VLAN_ID:            'vlan id error.',
    ERR_VM_UUID:            'vm uuid error.',
    ERR_VM_DEFINE:          'vm define error.',
    ERR_VM_OP:              'vm opperation error.',
    ERR_VM_NO_OP:         'op name error.',
    ERR_ARGS_VM_VCPU:       'vm args vcpu error.',
    ERR_ARGS_VM_MEM:       'vm args memory error.',
    ERR_ARGS_VM_EDIT_NONE:  'no args error.',
    ERR_VM_EDIT_REMARKS:    'edit remarks of vm error.',
    ERR_VM_EDIT:       'edit vm error.',
    ERR_VM_MIGRATE:         'migrate error.'
}