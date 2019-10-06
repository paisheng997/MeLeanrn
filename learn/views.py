from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.

###搜索条件的保存
def index(request):
    import copy
    parars = copy.deepcopy(request.GET)
    print(parars.urlencode())
    parars['xxxx'] = 123
    print(parars.urlencode())
    return HttpResponse('ok')
def md5(pwd):
    import time
    import hashlib
    ctime = str(time.time())
    m = hashlib.md5(bytes(pwd,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    res = m.hexdigest()
    return res

from rest_framework.views import APIView
from django.http import JsonResponse
from .models import *
from rest_framework import exceptions

ORDER_DICT = {
    1:{
        'name':'媳妇',
        'age':18,
        'gender':'女',
        'content':'.....'
    },
    2:{
            'name':'老狗',
            'age':18,
            'gender':'男',
            'content':'.....'
        }
}
from learn.utils import tro
class AuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        # self.dispatch()
        ret = {'code':1000,'msg':None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = UserInfo.objects.filter(username=user,password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            else:
                token = md5(pwd)
                UserToken.objects.update_or_create(user=obj,defaults={'token':token})
                ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求出错'
        return JsonResponse(ret)


class OrderView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [tro.VisitThrottle]
    def get(self,request):
        # self.dispatch()
        ret = {'code':1000,'msg':None,'data':None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)
class InfoView(APIView):
    def get(self,request):
        # print(request.user)
        # print(request.auth)
        return HttpResponse('用户详细信息')


from rest_framework.request import Request
from rest_framework.versioning import BaseVersioning
from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning
class ParamVerson():
    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        return version
class UserView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    versioning_class = QueryParameterVersioning
    def get(self,request):
        # self.dispatch()
        # request.query_params.get('')
        print(request.version)
        return HttpResponse('用户列表')
class DjangoView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    versioning_class = QueryParameterVersioning
    def get(self,request):
        from django.core.handlers.wsgi import WSGIRequest
        print(type(request._request))
        return HttpResponse('用户列表')

from rest_framework.parsers import JSONParser,FormParser
class ParserView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    versioning_class = QueryParameterVersioning
    # parser_classes = [JSONParser,FormParser]
    ## 表示只能解析 content-type :application/json头
    ##Formpaser 能解析 Content-Type: application/x-www-form-urlencoded头
    # 允许用户发送json数据 content-type:application/json {name:'',age:12}  传统的Django的请求头 与数据必须跟Django学习总结上面的一样
    def post(self,request):
        # 获取解析的数据
        '''
        1,获取用户请求
        2，获取用户请求体
        3，根据用户请求头 和 parser_classes = [JSONParser,FormParser] 中支持的请求头进行比较
        4，然后解析
        5，request.data
        '''
        print(request.data)
        # self.dispatch()
        return HttpResponse('用户列表')

import json
from rest_framework import serializers
class RolesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
from .models import *
class JsonView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    def get(self,request):
        # 方式1
        # ret = Role.objects.all().values('id','title')
        # ret = list(ret)
        # ret = json.dumps(ret,ensure_ascii=False)
        # 方式2 [obj,obj]
        # roles = Role.objects.all()
        # ser = RolesSerializer(instance=roles,many=True)
        # ret = json.dumps(ser.data,ensure_ascii=False)

        # 对于单个对象的
        role = Role.objects.all().first()
        ser = RolesSerializer(instance=role,many=False)
        ret = json.dumps(ser.data,ensure_ascii=False)

        return HttpResponse(ret)



# 序列化
# class MyUserInfo(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#     # aaa = serializers.IntegerField(source='user_type')
#     # choices
#     aaa = serializers.CharField(source='get_user_type_display')
#     # foreign
#     gp = serializers.CharField(source='group.id')
#     # mangtomany
#     roles = serializers.SerializerMethodField()
#     def get_roles(self,row):
#         role_list = row.roles.all()
#         ret = []
#         for item in role_list:
#             ret.append({'id':item.id,'title':item.title})
#         return ret
# class MyUserInfo(serializers.ModelSerializer):
#     aaa = serializers.CharField(source='get_user_type_display')
#     roles = serializers.SerializerMethodField()
#     group = serializers.CharField(source='group.title')
#     class Meta:
#         model = UserInfo
#         # 所有的字段
#         # fields = '__all__'
#         fields = ['id','username','aaa','roles','group']
#         # extra_kwargs = {'group':{'source':'group.title'},}
#     def get_roles(self,row):
#         role_list = row.roles.all()
#         ret = []
#         for item in role_list:
#             ret.append({'id':item.id,'title':item.title})
#         return ret
class MyUserInfo(serializers.ModelSerializer):
    # 反向生成url
    group = serializers.HyperlinkedIdentityField(view_name='uuu',lookup_field='group_id',lookup_url_kwarg='pk')
    class Meta:
        model = UserInfo
        # fields = '__all__'
        fields = ['id','username','password','group','roles']
        # 会影响效率 0-10 3,4层已经很大了
        # depth = 1
        depth = 0
class UserInfoView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    def get(self,request):
        userinfo = UserInfo.objects.all()
        ret = MyUserInfo(instance=userinfo,many=True,context={'request': request})
        # print(ret.data)
        ret = json.dumps(ret.data,ensure_ascii=False)
        return HttpResponse(ret)
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'
class GroupView(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        obj = UserGroup.objects.filter(id=pk).first()
        ser = GroupSerializer(instance=obj,many=False)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


#########################验证 ###############################
class xxx():
    def __init__(self,base):
        self.base = base
    def __call__(self, value):
        if not value.startswith(self.base):
            message = '标题必须以 %s 开头' %self.base
            raise serializers.ValidationError(message)
class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required':'标题不能为空'},validators=[xxx('老男人'),])
class UserGroupView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    def post(self,request,*args,**kwargs):
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
        else:
            print(ser.errors)
        return HttpResponse('ok')


###################################分页##############################
from learn.utils.serializers.pager import Pager1Serializer
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination
class MyPageNumberPagination(PageNumberPagination):
    # 每页显示多少
    page_size = 2
    #控制每页显示多少
    page_size_query_param = 'size'
    # 最大一页显示多少
    max_page_size = 5

    page_query_param = 'page'

class MYLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = None

# 加密分页
class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 2
    ordering = 'id'
    page_size_query_param = None
    max_page_size = None

class Pager1View(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    def get(self,request,*args,**kwargs):
        roles = Role.objects.all()
        pg = MyCursorPagination()
        pager_roles = pg.paginate_queryset(queryset=roles,request=request,view=self)
        ser = Pager1Serializer(instance=pager_roles,many=True)
        ret = json.dumps(ser.data,ensure_ascii=False)
        # return HttpResponse(ret)
        return pg.get_paginated_response(ser.data)

###############################视图#############################
from rest_framework.generics import GenericAPIView
class View1View(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    queryset = Role.objects.all()
    serializer_class = Pager1Serializer
    pagination_class = PageNumberPagination
    def get(self,request,*args,**kwargs):
        roles = self.get_queryset()
        pager_roles = self.paginate_queryset(roles)
        ser = self.get_serializer(instance=pager_roles,many=True)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)

from rest_framework.viewsets import GenericViewSet,ModelViewSet
class View2View(GenericViewSet):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    queryset = Role.objects.all()
    serializer_class = Pager1Serializer
    pagination_class = PageNumberPagination
    def list(self,request,*args,**kwargs):
        roles = self.get_queryset()
        pager_roles = self.paginate_queryset(roles)
        ser = self.get_serializer(instance=pager_roles,many=True)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


class View3View(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    queryset = Role.objects.all()
    serializer_class = Pager1Serializer
    pagination_class = PageNumberPagination


#######################################Contenttype##################

def test(request):
    # obj = Course.objects.filter(title='vue').first()
    # PricePolicy.objects.create(price=30,period=30,content_object=obj)
    # obj = Course.objects.filter(title='vue').first()
    # PricePolicy.objects.create(price=40, period=50, content_object=obj)
    # obj = Course.objects.filter(title='vue').first()
    # PricePolicy.objects.create(price=50, period=60, content_object=obj)

    obj1 = Course.objects.filter(title='vue').first()
    print(obj1)
    print(obj1.price_policy_list)
    print(obj1.price_policy_list.all())
    # price_polys = obj1.price_policy_list.all()
    # print(price_polys)
    return HttpResponse('ok')