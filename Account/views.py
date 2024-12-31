from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_list_or_404

import Destination.models
from .models import AccountModel
from .serializer import AccountSerializer
from rest_framework import status, generics
from Destination.models import DestinationModel
# Create your views here.

def deleteDestination(token):
    try:
        des_mod = DestinationModel.objects.get(app_sectet=token)
    except DestinationModel.DoesNotExist:
        print("no destination found for the given token")
    des_mod.delete()
class AccountViews(APIView):
    def get(self, request):
        acc_data = AccountModel.objects.all()
        acc_ser = AccountSerializer(acc_data, many=True).data
        return Response(acc_ser, status=status.HTTP_200_OK)
    def post(self, request):
        acc_ser = AccountSerializer(data=request.data)
        if acc_ser.is_valid():
            acc_ser.save()
            return Response({"message":"data added"}, status=status.HTTP_201_CREATED)
        return Response(acc_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, email):
        try:
            acc_mod = AccountModel.objects.get(email=email)
        except AccountModel.DoesNotExist:
            return Response({"message":"account not found for the given query"}, status=status.HTTP_404_NOT_FOUND)
        acc_ser = AccountSerializer(acc_mod, data = request.data)
        if acc_ser.is_valid():
            acc_ser.save()
            return Response({"message":"account updated successfully"}, status=status.HTTP_201_CREATED)
        return Response(acc_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, email):
        try:
            acc_mod = AccountModel.objects.get(email = email)
        except AccountModel.DoesNotExist:
            
            return Response({"message":"account not found for the given query"}, status=status.HTTP_404_NOT_FOUND)
        token = acc_mod.app_secret_token
        deleteDestination(token)
        acc_mod.delete()
        
        return Response({"message":"account deleted successfully"})






    

