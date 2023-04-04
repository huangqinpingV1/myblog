#!/usr/bin/env python
#ecoding:utf-8
#自定义中间件
import time
from ipware import get_client_ip
from user_agents import parse


class OnlineMiddleware(object):
    def __init__(self,get_response= None):
        self.get_response = get_response
        print("__init__() enter")
        super().__init__()

    def __call__(self,request):
        """page render time"""
        start_time = time.time()
        response =self.get_response(request)
        http_user_agent = request.META.get('HTTP_USER_AGENT','')
        ip,_ =get_client_ip(request)
        user_agent = parse(http_user_agent)
        print("ua  ="+str(user_agent)+",ip = "+str(ip))
        if not response.streaming:
            try:
                cast_time = 0.921
                if self.__dict__ and 'start_time' in self.__dict__:
                    cast_time = time.time() - self.start_time
                response.content = response.content.replace(b'<!!LOAD_TIMES!!>',str.encode(str(cast_time)[:5]))
            except Exception as e:
                print("Error OnlineMiddleware:%s" % e)
        return response
