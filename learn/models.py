from django.db import models

# Create your models here.
class UserGroup(models.Model):
    title = models.CharField(max_length=32)
class Role(models.Model):
    title = models.CharField(max_length=32)
class UserInfo(models.Model):
    user_type_choices = (
        (1,'普通用户'),
        (2,'vip'),
        (3,'svip'),
    )
    username = models.CharField(max_length=12)
    password = models.CharField(max_length=12)
    user_type = models.IntegerField(choices=user_type_choices)
    group = models.ForeignKey(to='UserGroup',on_delete=models.PROTECT)
    roles = models.ManyToManyField(to='Role')
class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo',on_delete=models.PROTECT)
    token = models.CharField(max_length=64)



##############################content type
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
class Course(models.Model):
    title = models.CharField(max_length=32)
    # 不生成字段仅用于反向查找
    price_policy_list = GenericRelation('PricePolicy')
class DegreeCourse(models.Model):
    title = models.CharField(max_length=32)
class PricePolicy(models.Model):
    price = models.IntegerField()
    period = models.IntegerField()
    # table_name = models.CharField(verbose_name='关联的表名称')
    # object_id = models.CharField(verbose_name='关联表中的数据行的id')

    # 该字段必须为content_type
    content_type = models.ForeignKey(ContentType,verbose_name='关联的表名称',on_delete=models.PROTECT)
    object_id = models.IntegerField(verbose_name='关联表中的数据行的id')
    content_object = GenericForeignKey('content_type','object_id')