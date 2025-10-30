from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if 'detail' in response.data and 'code' in response.data:
            response.data = {'detail': response.data['detail']}

    return response

