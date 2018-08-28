# coding=utf-8
from django.conf import settings
from django.core.cache import cache

LANGUAGE_CACHE_KEY = '_language'


def get_cache_language():
    return cache.get(LANGUAGE_CACHE_KEY, settings.LANGUAGE_CODE)


def set_cache_language(language_code):
    return cache.set(LANGUAGE_CACHE_KEY, language_code)
