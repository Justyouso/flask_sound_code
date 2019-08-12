# -*- coding: utf-8 -*-
# @Author: wangchao
# @Time: 19-8-12 上午10:26

import os, sys

environ = {}
environ[
    'PATH_INFO'] = "/home/justyouso/space/workspace/python/flask_sound_code/flask_uwsgi/"
environ['wsgi.version'] = (1, 0)
environ['wsgi.url_scheme'] = 'http'
environ['wsgi.input'] = sys.stdin
environ['wsgi.errors'] = sys.stderr
environ['wsgi.multithread'] = False
environ['wsgi.multiprocess'] = True
environ['wsgi.run_once'] = True


# 应用程序端(提供业务逻辑处理)
# uwsgi协议标准程序
def application(environ, start_response):
    # response_body = "The request method was %s" % environ['REQUEST_METHOD']
    response_body = "这是应用程序端"
    status = "200 OK"
    response_headers = [('Content-Type', 'test/plain'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]


# 服务程序端(提供 wsgi server)
# 服务端提供环境变量
# def run_with_cgi(application):
#     environ = dict(os.environ.items())
#     environ['wsgi.input'] = sys.stdin
#     environ['wsgi.errors'] = sys.stderr
#     environ['wsgi.version'] = (1, 0)
#     environ['wsgi.multithread'] = False
#     environ['wsgi.multiprocess'] = True
#     environ['wsgi.run_once'] = True
#     environ['wsgi.url_scheme'] = 'http'
#
#     headers_set = []
#     headers_sent = []
#
#     # 把应答的结果输出到终端
#     def write(data):
#         sys.stdout.write(data)
#         sys.stdout.flush()
#
#     def start_response(status, response_headers, exc_info=None):
#         headers_sent[:] = [status, response_headers]
#         return write
#
#     result = application(environ, start_response)
#
#     try:
#         for data in result:
#             if data:
#                 write(data)
#     finally:
#         if hasattr(result, 'close'):
#             result.close()
#
# run_with_cgi(application=application)

def write(data):
    sys.stdout.write(data)
    sys.stdout.flush()


def start_response(status, response_headers, exc_info=None):
    headers_sent = [status, response_headers]
    return write


# 中间层(middleware,路由分发)
class Router(object):
    def __init__(self):
        self.path_info = {}

    def route(self, environ, start_response):
        application = self.path_info[environ["PATH_INFO"]]
        return application(environ, start_response)

    def __call__(self, path):
        def wrapper(application):
            self.path_info[path] = application

        return wrapper


router = Router()


@router('/hello')
def hello(environ, start_response):
    status = '200 OK'
    output = 'Hello'
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    write = start_response(status, response_headers)
    return [output]


environ = {
    "PATH_INFO": "/hello"}
result = router.route(environ, start_response)

for value in result:
    write(value)
