#!/usr/bin/env python
#ecoding:utf-8
#自定义中间件
import time
from ipware.ip import get_real_ip
from django.core.cache import cache

class OnlineMiddleware(object):
    def process_request(self,request):
        self.start_time = time.time()
    
    def process_view(self,request,view_func,view_args,view_kwargs):
        """
        处理当前在线认数
        """
        http_user_agent = request.META.get('HTTP_USER_AGENT',[])
        if 'Spider' in http_user_agent or 'spider' in http_user_agent:
            return 
        online_ips = cache.get("online_ips",[])

        if online_ips:
            online_ips = cache.get_many(online_ips).keys()

        ip = get_real_ip(request) 
        cache.set(ip,0,5*60)

        if ip not in online_ips:
            oline_ips.append(ip)
        
        cache.set("online_lips",online_ips)

   def process_response(self,request,response):
       cast_time = time.time() -self.start_time
       response.content = response.replace(b'<!!LOAD_TIMES!!>',str.encode(str(cast_time)[:5]))
       return response
