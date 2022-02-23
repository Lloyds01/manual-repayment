from logging import raiseExceptions
import random
import string
import jwt
from rest_framework import generics
from .models import CustomUser
from .models import Jwt, LoanRepayment
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from .serializers import ChangePasswordSerializer, LoginSerializer, RegisterSerializer, RepaymentSerializer, ResfreshSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from .authentication import Authentication



def get_random(lenght):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=lenght))

def get_access_token(payload):
    return jwt.encode(
        {'exp': datetime.now() + timedelta(minutes=5), **payload},    #set expiry time for the access token 
        settings.SECRET_KEY,        #a secret that is unique to your app
        algorithm="HS256"      #lenght of jwt token 
    )

def get_refresh_token():
     return jwt.encode(
        {'exp': datetime.now() + timedelta(days=365), 'data':get_random(10)},    #set expiry time for the access token 
        settings.SECRET_KEY,        #a secret that is unique to your app
        algorithm="HS256"      #lenght of jwt token 
     )

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data) #request the serialized data
        serializer.is_valid(raise_exception=True)  #validate serializer
        print(serializer.validated_data)
        user =authenticate(
            username=serializer.validated_data["email"], 
            password=serializer.validated_data['password']) #checking if user exist and log them in

        if not user:
            return Response({'error':'invalid email or password'}, status="400")

        Jwt.objects.filter(user_id=user.id).delete()    #validation and delete 

        access = get_access_token({'user_id': user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(
            user_id =user.id,access=access.decode(), refresh = refresh.decode())

        return Response({'access': access, 'refresh':refresh})


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data) #request the serialized data
        serializer.is_valid(raise_exception=True)  #validate serializer

        CustomUser.objects._create_user(**serializer.validated_data)

        return Response({'success': 'User created'})



class RefreshView(APIView):
    serializer_class = ResfreshSerializer

    def post (self, request):
        serializer =self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(
                refresh = serializer.validated_data['refresh'])
        except Jwt.DoesNotExist:
            return Response({'error':'refresh token not found'}, status='400')

        if not Authentication.verify_token(serializer.validated_data['refresh']):
            return Response ({'error': 'Token is invalid or has expired'})

#update current loggedin user and  return a new access token and refresh token 
        access = get_access_token({'user_id': active_jwt.user.id})
        refresh = get_refresh_token()

        active_jwt.access= access.decode()
        active_jwt.refresh= refresh.decode()
        active_jwt.save()
        return Response({'access': access, 'refresh':refresh})



    

class Getsecuredinfo(APIView): 
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        return Response({'data': 'this is a secured info'})


class Repayment(generics.ListCreateAPIView):
    queryset = LoanRepayment.objects.all()
    serializer_class = RepaymentSerializer

    def approved_repayment(self,request, queryset=None):
        if request.method == "GET":
            approved = LoanRepayment.objects.filter(is_approved = True)
            serializer = RepaymentSerializer(approved, many=True)
            print("--------------------")
            print(serializer.data)
            return Response(serializer.data)

    def pending_repayment(self, request, queryset=None):
        if request.method == "GET":
            pending = LoanRepayment.objects.filter(is_approved = False)
            serializer = RepaymentSerializer(pending, many=True)
            print("--------------------")
            print(serializer.data)
            return Response(serializer.data)

class Changepassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj =self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(self):
            #check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                #set password hashes te password tat user will get
                self.object.set_password(serializer.data.get('new_password'))  

                self.object.save()
                response = {
                    'status':'success',
                    'code':status.HTTP_200_OK,

                    'messahe':'password updated successfully',

                    'data':[]
                }
                return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def approved_repayment(request):
    if request.method == "GET":
        approved = LoanRepayment.objects.filter(is_approved = True)
        serializer = RepaymentSerializer(approved, many=True)
        print("--------------------")
        print(serializer.data)
        return Response(serializer.data)


@api_view(['GET'])
def pending_repayment(request):
    if request.method == "GET":
        pending = LoanRepayment.objects.filter(is_approved = False)
        serializer = RepaymentSerializer(pending, many=True)
        print("--------------------")
        print(serializer.data)
        return Response(serializer.data)


# def approve_repayment(request):

#     if request.method == 'POST':
#         pending = LoanRepayment.objects.filter(is_approved = False)
#         approve = 








