from django.shortcuts import render

from api.serializers import UserSerializer
from api.serializers import TodoSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import authentication,permissions
from rest_framework import serializers

from remainder.models import Todos


class SignUpView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class TodoView(ViewSet):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def create(self,request,*args,**kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializer(qs)
        return Response(data=serializer.data)    
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        if qs.user==request.user:
            qs.delete()
            return Response(data={"message":"deleted"})
        else:    
            raise serializers.ValidationError("permission denied")
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=todo_object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    

class TodoViewsetView(ModelViewSet):

    queryset=Todos.objects.all()
    serializer_class=TodoSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


