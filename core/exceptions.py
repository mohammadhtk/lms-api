from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

# Custom exception handler that provides consistent error responses.
def custom_exception_handler(exc, context):
    
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': True,
            'message': str(exc),
            'details': response.data
        }
        response.data = custom_response_data

    return response


# Custom exception for business logic errors.
class BusinessLogicException(Exception):
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
