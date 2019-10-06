# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from learn.models import *
class Pager1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'