# coding=utf-8
'''
@author: bob

系统通过中间件将session或cookie中的语言信息写入cache
在代码中只需要直接从cache中获取就行
'''
from django.utils.translation import get_language as django_get_language
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.conf import settings
from django.core.cache import cache

URL_LANGUAGE_LEY = '_language'


def get_language(request):
    lang = request.GET.get(URL_LANGUAGE_LEY)

    if not lang and hasattr(request, 'session'):
        lang = request.session.get(LANGUAGE_SESSION_KEY, None)

    if not lang:
        lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, None)

    if not lang:
            lang = settings.LANGUAGE_CODE

    return lang

