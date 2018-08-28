#coding=utf-8

from django.contrib.auth.models import User 

def add_users(username_prefix="test",count=1,default_email="xxxx@innervm.innervm",vm_limit=3):
    print ("批量添加用户")
    res = []
    for i in range(count):
        user_name = username_prefix + str(i)
        d = {"user_name":user_name}
        print ("用户名："+user_name)
        if not User.objects.filter(username=user_name).exists():
            uobj = User()
            uobj.email = default_email
            uobj.username = user_name
            #uobj.interclient_enable = True
            uobj.first_name = user_name
            uobj.set_password(user_name)
            uobj.vm_limit = vm_limit
            uobj.save()
            print ("成功")
            d["msg"] = "成功"
        else:
            print ("已存在")
            d["msg"] = "已存在"
        res.append(d)


