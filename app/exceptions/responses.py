from app.schemas.errors import ErrorResponse


def error_response(description: str, message: str) -> dict:
    return {
        'model': ErrorResponse,
        'description': description,
        'content': {
            'application/json': {
                'example': {
                    'details': {
                        'optional': {},
                    },
                    'message': message,
                },
            },
        },
    }


bad_request_response = {
    400: error_response('Bad Request', 'Bad request'),
}

unauthorized_response = {
    401: error_response('Unauthorized', 'Unauthorized'),
}

forbidden_response = {
    403: error_response('Forbidden', 'Access denied'),
}

not_found_response = {
    404: error_response('Not Found', 'Not found'),
}

conflict_response = {
    409: error_response('Conflict', 'Conflict'),
}

validation_error_response = {
    422: error_response('Validation Error', 'Validation error'),
}

internal_server_error_response = {
    500: error_response('Internal Server Error', 'Internal server error'),
}

auth_responses = {
    **bad_request_response,
    **unauthorized_response,
    **forbidden_response,
    **conflict_response,
    **validation_error_response,
    **internal_server_error_response,
}

common_error_responses = {
    **bad_request_response,
    **unauthorized_response,
    **forbidden_response,
    **not_found_response,
    **validation_error_response,
    **internal_server_error_response,
}

create_error_responses = {
    **bad_request_response,
    **unauthorized_response,
    **forbidden_response,
    **conflict_response,
    **validation_error_response,
    **internal_server_error_response,
}