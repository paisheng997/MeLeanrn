from django.urls import path,re_path,include
from .views import *
from django.conf.urls import url

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'xxx',View3View)

urlpatterns = [
    path('test/',test),
    path('login/',AuthView.as_view()),
    path('order/',OrderView.as_view()),
    path('info/',InfoView.as_view()),
    path('userview/',UserView.as_view()),
    path('django/',DjangoView.as_view()),
    path('parser/',ParserView.as_view()),
    path('userinfo/',UserInfoView.as_view()),
    path('usergroup/',UserGroupView.as_view()),
    path('pager1/',Pager1View.as_view()),
    path('view1/',View1View.as_view()),
    path('view2/',View2View.as_view({'get':'list'})),
    re_path('view3/(?P<pk>\d+)',View3View.as_view({'get':'retrieve','post':'create','put':'update','delete':'destroy'})),
    re_path('userinfo/(?P<pk>\d+)',GroupView.as_view(),name='uuu'),
    # url(r'^(?P<version>[v1|v2]+)/userview/$',UserView.as_view()),

    path('',include(router.urls))
]