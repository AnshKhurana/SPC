from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status, generics

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class SnippetList(APIView):
#     def get(self,request,format=None):
#         snippets=Snippet.objects.all()
#         serializer=SnippetSerializer(snippets,many=\
#                                      True)
#         return Response(serializer.data)
#     def post(self,request,format=None):
#         serializer=SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# class SnippetDetail(APIView):
#     def get_object(self,pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#     def get(self,request,pk,format=None):
#         snippet=self.get_object(pk)
#         serializer=SnippetSerializer(snippet)
#         return Response(serializer.data)
#     def put(self,request,pk,format=None):
#         snippet=self.get_object(pk)
#         serializer=SnippetSerializer(snippet,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk,format=None):
#         snippet=self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# mixins see if you want

class SnippetList(generics.ListCreateAPIView):
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
class SnippetDetail(generics.RetrieveDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


@csrf_exempt
@api_view(['GET','POST'])
def snippet_list(request,format=None):
    if request.method=='GET':
        snippets=Snippet.objects.all()
        serializer=SnippetSerializer(snippets,many=True)
        # return JsonResponse(serializer.data,safe=False)
        return Response(serializer.data)
    elif request.method=='POST':
        # print("hello very god")
        serializer=SnippetSerializer(data=request.data)
        # print('yo')
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data,status=201)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def snippet_detail(request,pk,format=None):
    try:
        snippet=Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        # return HttpResponse(status=404)
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=SnippetSerializer(snippet)
        return Response(serializer.data)
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializer=SnippetSerializer(snippet,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    elif request.method=='DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
