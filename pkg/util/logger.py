# import os
# import time

# from uuid import uuid4
# import simplejson as json

# from django.http import QueryDict
# from rest_framework import status
# from logging.handlers import TimedRotatingFileHandler

# from pkg.setting import setting


# class Log(object):
#     INFO_TYPE = 'info'
#     WARN_TYPE = 'warn'
#     ERROR_TYPE = 'error'
#     SLOW_TYPE = 'slow'

#     LOG_FUNC_MAP = {
#         INFO_TYPE: setting.info_log.info,
#         WARN_TYPE: setting.warn_log.info,
#         ERROR_TYPE: setting.error_log.info,
#         SLOW_TYPE: setting.slow_log.info,
#     }

#     def __init__(self, request):
#         # Basic information
#         self._level = self.INFO_TYPE
#         self._trace_id = request.META.get('HTTP_X_TRACE_ID') or uuid4().hex[:16]
#         self._created_at = int(time.time())
#         self._cost_time = time.time()

#         # Business information
#         self._service = setting.SERVER_NAME
#         self._hostname = setting.SERVER_HOSTNAME
#         self.business = ''
#         self._business_info = {}
#         self._stacktrace = ''

#         # HTTP request information
#         self._client_ip = request.request_ip
#         self._host = request.request_host
#         self._method = request.method
#         self._uri = request.get_full_path()
#         self._request_data = {}
#         self._status_code = status.HTTP_200_OK
#         self._response_data = {}

#     @property
#     def request_data(self):
#         return self._request_data

#     @request_data.setter
#     def request_data(self, value):
#         self._request_data.update(self._parser_data(value))

#     @property
#     def response_data(self):
#         return self._response_data

#     @response_data.setter
#     def response_data(self, value):
#         self._response_data.update(self._parser_data(value))

#     @staticmethod
#     def _parser_data(value):
#         if isinstance(value, bytes):
#             try:
#                 data = json.loads(value)
#                 if isinstance(data, dict):
#                     return data
#                 raise ValueError()
#             except ValueError or TypeError:
#                 return {'data': value}
#         elif isinstance(value, str) or isinstance(value, list):
#             return {'data': value}
#         elif isinstance(value, dict):
#             return value
#         elif isinstance(value, QueryDict):
#             return dict(value)
#         return {}

#     def _json(self):
#         data = {
#             'level': self._level,
#             'trace_id': self._trace_id,
#             'created_at': self._created_at,
#             'cost_time': self._cost_time,
#             'service': self._service,
#             'business': self.business,
#             'hostname': self._hostname,
#             'messages': {
#                 'client_ip': self._client_ip,
#                 'host': self._host,
#                 'uri': self._uri,
#                 'method': self._method,
#                 'request': self._request_data,
#                 'status_code': self._status_code,
#                 'response': self._response_data,
#             }
#         }
#         data['messages'].update(self._business_info)
#         if self._stacktrace:
#             data['messages']['stacktrace'] = self._stacktrace
#         return json.dumps(data)

#     def update(self, response):
#         """
#        Update log level, HTTP response data and time consuming
#        """
#         if not self.business:
#             return
#         self._status_code = response.status_code
#         self.response_data = response.content

#         # Update log cost time
#         self._cost_time = int((time.time() - self._cost_time) * 1000)

#         # Update log level
#         if self._status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
#             self._level = self.ERROR_TYPE
#             if hasattr(response, 'stacktrace'):
#                 self._stacktrace = response.stacktrace
#         elif self._status_code < status.HTTP_200_OK or self._status_code >= status.HTTP_300_MULTIPLE_CHOICES:
#             self._level = self.WARN_TYPE
#         elif self._cost_time > setting.SERVER_LOG_SLOW_TIME:
#             self._level = self.SLOW_TYPE

#     def record(self):
#         """
#         Record message in location file
#         """
#         if not self.business:
#             return
#         self.LOG_FUNC_MAP[self._level](self._json())


# class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):

#     @property
#     def dfn(self):
#         currentTime = int(time.time())
#         # get the time that this sequence started at and make it a TimeTuple
#         dstNow = time.localtime(currentTime)[-1]
#         t = self.rolloverAt - self.interval
#         if self.utc:
#             timeTuple = time.gmtime(t)
#         else:
#             timeTuple = time.localtime(t)
#             dstThen = timeTuple[-1]
#             if dstNow != dstThen:
#                 if dstNow:
#                     addend = 3600
#                 else:
#                     addend = -3600
#                 timeTuple = time.localtime(t + addend)
#         dfn = self.rotation_filename(self.baseFilename + "." + time.strftime(self.suffix, timeTuple))

#         return dfn

#     def shouldRollover(self, record):
#         """
#         Determine if rollover should occur.

#         record is not used, as we are just comparing times, but it is needed so
#         the method signatures are the same
#         """
#         dfn = self.dfn
#         t = int(time.time())
#         if t >= self.rolloverAt or os.path.exists(dfn):
#             return 1
#         return 0

#     def doRollover(self):
#         """
#         do a rollover; in this case, a date/time stamp is appended to the filename
#         when the rollover happens.  However, you want the file to be named for the
#         start of the interval, not the current time.  If there is a backup count,
#         then we have to get a list of matching filenames, sort them and remove
#         the one with the oldest suffix.
#         """
#         if self.stream:
#             self.stream.close()
#             self.stream = None
#         # get the time that this sequence started at and make it a TimeTuple
#         dfn = self.dfn
#         if not os.path.exists(dfn):
#             self.rotate(self.baseFilename, dfn)
#         if self.backupCount > 0:
#             for s in self.getFilesToDelete():
#                 os.remove(s)
#         if not self.delay:
#             self.stream = self._open()
#         currentTime = int(time.time())
#         newRolloverAt = self.computeRollover(currentTime)
#         while newRolloverAt <= currentTime:
#             newRolloverAt = newRolloverAt + self.interval
#         # If DST changes and midnight or weekly rollover, adjust for this.
#         if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
#             dstAtRollover = time.localtime(newRolloverAt)[-1]
#             dstNow = time.localtime(currentTime)[-1]
#             if dstNow != dstAtRollover:
#                 if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
#                     addend = -3600
#                 else:           # DST bows out before next rollover, so we need to add an hour
#                     addend = 3600
#                 newRolloverAt += addend
#         self.rolloverAt = newRolloverAt
