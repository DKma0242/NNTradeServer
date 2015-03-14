import json
from django.http import HttpResponse


ERRNO_NO_ERROR = 0
ERRNO_INVALID_REQUEST_METHOD = -1
ERRNO_MISSING_PARAMETER = -2

ERRNO_USERNAME_EXIST = -1000
ERRNO_USERNAME_NON_EXIST = -1001
ERRNO_MISMATCH_USERNAME_PASSWORD = -1002
ERRNO_NO_TOKEN = -1003
ERRNO_MISMATCH_TOKEN = -1004


def response_with_erron(erron):
    if erron == ERRNO_NO_ERROR:
        return HttpResponse(json.dumps({'success': True, 'errno': erron}))
    return HttpResponse(json.dumps({'success': False, 'errno': erron}))
