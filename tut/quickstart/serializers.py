# from django.contrib.auth.models import User,Group
# from rest_framework import serializers
# class UserSerializer(serializers.HyperlinkedModelSerializers):
# 	class Meta:
# 		model=User
# 		fields=('url','username','email','groups')
# class GroupSerializer(serializers.HyperlinkedModelSerializers):
# 	class Meta:
# 		model=Groupfields=('url','name')
# 		
from rest_framework import serializers
from .models import employees

class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=employees
        # fields=('firstname','lastname')
        fields='__all__'

