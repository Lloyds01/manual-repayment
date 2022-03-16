import email
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
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from .authentication import Authentication



@staticmethod
def check_repayment(request):
    if request.method == "POST":
        serializer = RepaymentSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        payment_date = serializer.validated_data["payment_date"]
        amount = serializer.validated_data["amount"]
        remita_manadate = serializer.validated_data["remita_manadate"]
        print(f'user input: payment data{payment_date}, amount: {amount}, remita_mandate{remita_manadate}')
        # is_flagged = (serializer.validated_data["is_flagged"])
        response = LoanRepayment.flag_repayment(payment_date, amount, remita_manadate)
        return response


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
        
        user = authenticate(
            email=serializer.validated_data["email"], 
            password=serializer.validated_data['password']) #checking if user exist and log them in
        
       
        if not user:
            
            return Response({'error':'invalid email or password'}, status="400")

        else:
            login(request, user)

        Jwt.objects.filter(user_id=user.id).delete()    #validation and delete 

        access = get_access_token({'user_id': user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(
            user_id = user.id,access=access.decode(), refresh = refresh.decode())


        # return Response({'user_email':user.email})
        return Response({'user_email':user.email,'access': access, 'refresh':refresh})



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
    
    def get_queryset(self):
        user = self.request.user
        return user.accounts.all()
    
    # queryset = LoanRepayment.objects.all()
    serializer_class = RepaymentSerializer

    

# @api_view(['POST'])
# def post_repayment(request):
#     if request.method == "POST":
#         serializer = RepaymentSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)

#         serializer.save()
#         message = {
#                 "status": "Created"
#             }
#         return Response(data=message, status='200')


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
        if serializer.is_valid():
            #check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                response = {
                    'status':'failed',
                    'code':status.HTTP_400_BAD_REQUEST,

                    'message':'password failed',

                    'data':[]
                }
                return Response(response)
            #set password hashes the password that user will get
            self.object.set_password(serializer.data.get('new_password'))  

            self.object.save()
            response = {
                'status':'success',
                'code':status.HTTP_200_OK,

                'message':'password updated successfully',

                'data':[]
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def approved_repayment(request):
    if request.method == "GET":
        approved = LoanRepayment.objects.filter(is_approved = True, is_mandate_closed = False)
        serializer = RepaymentSerializer(approved, many=True)
        
        print(serializer.data)
        return Response(serializer.data)


@api_view(['GET'])
def pending_repayment(request):
    if request.method == "GET":
        pending = LoanRepayment.objects.filter(is_approved = False)
        serializer = RepaymentSerializer(pending, many=True)
        
        print(serializer.data)
        return Response(serializer.data)

    
@api_view(['POST'])
def Approve_one(request):
    if request.method == "POST":
        serializer = ApproveoneSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user_designation = serializer.validated_data["is_staff"]
        payment_id = int(serializer.validated_data["payment_id"])
        is_approved = serializer.validated_data["is_approved"]
        email = serializer.validated_data["email"]
        user = CustomUser.objects.filter(email=email, is_staff = user_designation)
        if user:
            
            print(user.values())
            loan = LoanRepayment.objects.filter(id=payment_id).update(is_approved=is_approved)
            print(loan)
            result = LoanRepayment.objects.filter(id=payment_id)
            
            print(result.values())
            response = {
                    'status':'success',
                    
                    'message':'payment approval updated'
                }
        else:
            response = {
                    'status':'unsuccessful',
                    
                    'message':'payment approval not successful'
                }
        return Response(data=response, status=status.HTTP_201_CREATED)
    
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Approve_all(request):
    if request.method == "POST":
        serializer = ApproveallSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user_designation = serializer.validated_data["is_staff"]
        approve_all = serializer.validated_data["is_approved_all"]
        email = serializer.validated_data["email"]
        user = CustomUser.objects.filter(email=email, is_staff = user_designation)
        if user and approve_all:
            
            print(user.values())
            loan = LoanRepayment.objects.filter(is_approved=False).update(is_approved=True)
            print(loan)
            response = {
                    'status':'success',
                    
                    'message':'all payment approved successfully'
                }
        else:
            response = {
                    'status':'unsuccessful',
                    
                    'message':'you do not have permission to carry out this action'
                }
        return Response(data=response, status=status.HTTP_201_CREATED)
    
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




