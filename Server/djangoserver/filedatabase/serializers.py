import json

from rest_framework import serializers
from filedatabase.models import FileRecord
from django.contrib.auth.models import User


class FileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = FileRecord
        fields = ('url', 'id', 'owner',
                  'file_name', 'file_type', 'file_data', 'md5sum')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    files = serializers.HyperlinkedRelatedField(many=True, view_name='filerecord-detail', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'files')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
