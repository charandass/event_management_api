from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from .helper import api_response, error_formator, check_auth
import traceback
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


        
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = RegisterSerializer(data = data)
            
            if serializer.is_valid():
                if User.objects.filter(username = serializer.data['username']).exists():
                    return JsonResponse(api_response(1,[],"Username is already taken",[])) 
                else:
                    user = User.objects.create(first_name=serializer.data['first_name'],
                                   last_name = serializer.data['last_name'],
                                   email = serializer.data['email'],
                                   username = serializer.data['username'].lower(),
                                   password = make_password(serializer.data['password'])
                                   )
                    
                    return JsonResponse(api_response(0,[],"User Account Created Successfully",[]))
            else:
                err = error_formator(serializer.errors)
                return JsonResponse(api_response(1,[],"Error",err))
                           
            
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return JsonResponse(api_response(1,[],"Error",str(e)))
            
            
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            
            if serializer.is_valid():
                user = User.objects.filter(username=serializer.data['username'])
                print(user[0].password)
                if not user.exists():
                    return JsonResponse(api_response(1,[],"account not found",[]))
                else:
                    if check_password(serializer.data['password'], user[0].password):
                        refresh = RefreshToken.for_user(user[0])
                        token = { 'token': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }}
                        return JsonResponse(api_response(0,token,"login Success",[]))
                    else:
                        return JsonResponse(api_response(0,[],"Wrong Credentials",[]))
            else:
                return JsonResponse(api_response(1,serializer.errors,"Something went wrong",[]))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return JsonResponse(api_response(1,[],"Error",str(e)))