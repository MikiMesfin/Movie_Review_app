from rest_framework.exceptions import APIException

class TMDBAPIError(APIException):
    status_code = 503
    default_detail = 'TMDB API service temporarily unavailable.'
    default_code = 'tmdb_service_unavailable' 