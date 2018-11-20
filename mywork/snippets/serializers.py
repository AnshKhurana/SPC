from rest_framework import serializers
from snippets.models import Snippet
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    snippets=serializers.PrimaryKeyRelatedField\
        (many=True,queryset=Snippet.objects.all())
    class Meta:
        model=User
        fields=('id','username','snippets')
class SnippetSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model=Snippet
        fields=('owner','stext','scom')

    # id=serializers.IntegerField(read_only=True)
    # stext=serializers.CharField(max_length=50)
    # scom=serializers.CharField(max_length=50)
    # def create(self,validated_data):
    #     return Snippet.objects.create(**validated_data)
    # def update(self,instance,validated_data):
    #     instance.stext=validated_data.get('stext',instance.stext)
    #     instance.scom=validated_data.get('scom',instance.scom)
    #     instance.save()
    #     return instance