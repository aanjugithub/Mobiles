from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class MobileListCreateView(APIView):
    def get(self,request,*args,**kwargs):
        return Response(data={"message":"Mobile list view impl"})
    
    def post(self,request,*args,**kwargs):
        return Response(data={"message":"mobile list post"})

#localhoost 8000/api/mobiles/{id}  
      
class MobileDetailUpdateDestroyView(APIView):
    
    def get(self,request,*args,**kwargs):
        return Response(data={"message":"get deatil of a specific item"})
    
    def put(self,request,*args,**kwargs):
        return Response(data={"message":"update an item"})
    
    def delete(self,request,*args,**kwargs):
        return Response(data={"message":"delete selected item"})
