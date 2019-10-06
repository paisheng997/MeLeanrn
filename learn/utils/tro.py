from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
VISIT_DICT = {}
import time
# 自定义的节流
'''
class VisitThrottle(object):
    def __init__(self):
        self.history = None
    def allow_request(self,request,views):
        ctime = time.time()
        remote_addr = request.META.get('REMOTE_ADDR')
        if remote_addr not in VISIT_DICT:
            VISIT_DICT[remote_addr] = [ctime]
            return True
        history = VISIT_DICT.get(remote_addr)
        self.history = history
        while history and history[-1] < ctime - 60:
            history.pop()
        if len(history) < 3:
            history.insert(0,ctime)
            return True
        return False
    def wait(self):
        return  60 - (time.time() - self.history[-1])
'''
class VisitThrottle(SimpleRateThrottle):
    scope = 'fcy'
    def get_cache_key(self, request, view):
        return self.get_ident(request)
class UserThrottle(SimpleRateThrottle):
    scope = 'fcy_user'
    def get_cache_key(self, request, view):
        return request.user.username