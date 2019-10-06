
from learn.models import *
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
class Authtication(BaseAuthentication):
    def authenticate(self,request):
        token = request._request.GET.get('token')
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return (token_obj.user,token_obj)
    # 认证失败时，返回给浏览器的响应头
    def authenticate_header(self,request):
        pass
class FirstAuthtication(BaseAuthentication):
    def authenticate(self,request):
        pass
    def authenticate_header(self,request):
        pass