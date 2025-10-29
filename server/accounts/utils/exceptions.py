from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if "detail" in response.data:
            response.data = {"message": response.data["detail"]}

        elif isinstance(response.data, dict):
            new_data = {}
            for key, value in response.data.items():
                if key == "detail":
                    new_data["message"] = value
                else:
                    new_data[key] = value
            response.data = new_data

    return response
