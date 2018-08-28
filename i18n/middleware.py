from django.conf import settings
from django.utils.translation import LANGUAGE_SESSION_KEY
from .api import get_language
from .cache import set_cache_language
import django

class RequestLanguageMiddleware(object):
    def process_request(self, request):
        language = get_language(request)
        request.session[LANGUAGE_SESSION_KEY] = language
        request.LANGUAGE_CODE = language
        set_cache_language(request.LANGUAGE_CODE)
        return None

    def process_response(self, request, response):
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, get_language(request), settings.LANGUAGE_COOKIE_TIMEOUT)
        return response
