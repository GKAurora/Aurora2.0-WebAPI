# from pkg.handlers import base
# from pkg.util.logger import Log
# from pkg.handlers.hello import (
#     Hello
# )
# from flask import request

# def _get_request_ip(request):
#     """
#     Returns the IP of the request, accounting for the possibility of being
#     behind a proxy.
#     """
#     request_ip = request.META.get('REMOTE_ADDR', '')
#     ips = request.META.get('HTTP_X_FORWARDED_FOR')
#     if ips:
#         # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
#         request_ip = ips.replace(' ', '').split(',')[0]
#     return request_ip

# APP = base.Aurora(__name__)

# @APP.before_request
# def process_request():
#     """
#     Initialize log content
#     """
#     # request._body = request.
#     request.request_host = request.META.get('HTTP_HOST')
#     request.request_ip = _get_request_ip(request)
#     request.log = Log(request)

# @APP.after_request
# def process_response(response):
#     """
#     Record log content
#     """
#     request.log.update(response)
#     request.log.record()
#     return response


# @APP.get("/hello")
# def hello():
#     return Hello.hello_w()
