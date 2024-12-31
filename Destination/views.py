from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializer import DestinationSerializer
from .models import DestinationModel
from rest_framework import status 
import requests
from Account.models import AccountModel 
from rest_framework.renderers import JSONRenderer
from uuid import UUID
# Create your views here.
class DestinationView(APIView):
    def get(self, request):
        des = DestinationModel.objects.all()
        des_ser = DestinationSerializer(des, many=True).data
        return Response(des_ser, status=status.HTTP_200_OK)
    def post(self, request):
        new_dest = DestinationSerializer(data=request.data) 
        if new_dest.is_valid():
            new_dest.save()
            return Response({"message":"Data is valid"}, status=status.HTTP_201_CREATED)
        return Response(new_dest.errors, status=status.HTTP_400_BAD_REQUEST)         

class DestinationById(APIView):
    def get(self, request, account_id):
        try:
            account = AccountModel.objects.get(account_id=account_id)
            destinations = DestinationModel.objects.filter(account=account)
            serializer = DestinationSerializer(destinations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccountModel.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)


class IncomingDataHandler(APIView):
    def post(self, request):
        try:
            token = request.headers.get('CL-X-TOKEN')
        except ValueError:
            return Response({"message":"not a valid token"}, status=status.HTTP_401_UNAUTHORIZED)
        if not token:
            return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            
            account = AccountModel.objects.get(app_secret_token=str(token)  )  
            
        except AccountModel.DoesNotExist:
            return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        for destination in account.destinations.all():
            headers = {
                "app_id":destination.app_id,
                "app_sectet":str(destination.app_sectet),
                "content_type":destination.content_type,
                "accept":destination.accept
            }
    
            url = destination.url
            method = destination.http_method

            try:
                if method == 'GET':
                    response = requests.get(url, params=data, headers=headers)
                elif method == 'POST':
                    response = requests.post(url, json=data, headers=headers)
                elif method == 'PUT':
                    response = requests.put(url, json=data, headers=headers)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Data sent to all destinations successfully"}, status=status.HTTP_200_OK)
    def get(self, request):
        return Response({"message":"invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request):
        return Response({"message":"invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request):
        return Response({"message":"invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # if request.method=='POST':
        
    # else:
    #     return Response({"message":"invalid data"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)