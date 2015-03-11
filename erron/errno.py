import json
from django.http import HttpResponse


ERRON_NO_ERROR = 0
ERROR_MISSING_PARAMETER = -1
ERROR_AUTHENTICATE = -2
ERRON_INVALID_REQUEST_METHOD = -3

ERRON_USERNAME_EXIST = -1000
ERRON_USERNAME_NON_EXIST = -1001
ERRON_MISMATCH_USERNAME_PASSWORD = -1002
ERRON_MISMATCH_TOKEN = -1003


def response_with_erron(erron):
    if erron == ERRON_NO_ERROR:
        return HttpResponse(json.dumps({'success': True, 'errno': erron}))
    return HttpResponse(json.dumps({'success': False, 'errno': erron}))


def response_missing_parameter():
    return response_with_erron(ERROR_MISSING_PARAMETER)


def response_invalid_request_method():
    return response_with_erron(ERRON_INVALID_REQUEST_METHOD)