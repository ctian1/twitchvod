# base error...
class HTTPError(Exception):
    """
    """

    def __init__(self, *args, **kwargs):
        self.http_response = kwargs.pop("http_response", None)
        super(HTTPError, self).__init__(*args, **kwargs)


# 4xx errors...
class HTTPClientError(HTTPError):
    """
    """


# 5xx errors...
class HTTPServerError(HTTPError):
    """
    """


# everything else...
class HTTPGenericError(HTTPError):
    """
    """
