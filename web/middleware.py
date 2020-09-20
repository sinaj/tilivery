def tilivery_middleware(get_response):

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.context = dict()

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware