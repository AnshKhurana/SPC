from django.contrib.auth.forms import UserCreationForm
import sqlite3
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views import generic
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from filedatabase.models import FileRecord
from filedatabase.permissions import IsOwner
from filedatabase.serializers import FileSerializer, UserSerializer
from rest_framework import generics, viewsets, renderers, status
from django.contrib.auth.models import User
from rest_framework import permissions


class FileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = FileRecord.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsOwner,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'filedatabase': reverse('file-list', request=request, format=format)
    })


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = '/schema'
    template_name = 'signup.html'



