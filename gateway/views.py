import email
from logging import raiseExceptions
import random
import stat
import string
import jwt
from rest_framework import generics
from .models import CustomUser
from .models import Jwt, LoanRepayment
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.db.models import Count


# for corsheaders issue on the frontend
@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data)  # request the serialized data
        serializer.is_valid(raise_exception=True)  # validate serializer

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data['password'])  # checking if user exist and log them in

        if not user:
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "invalid email or password. Please try again!!"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            login(request, user)
            # create a token for user for identification
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "status": status.HTTP_200_OK,
                "user_email": user.email,
                "token": token.key
            }
            # return the email and token
            return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_logout(request):

    Token.objects.get(user=request.user).delete()

    logout(request)
    data = {
        "status": status.HTTP_200_OK,
        "message": "logout successful"
    }

    return Response(data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class Repayment(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = LoanRepayment.objects.all()
    serializer_class = PostRepaymentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        # user_id = serializer.validated_data.get('id')
        phone = serializer.validated_data.get('phone')
        amount = serializer.validated_data.get('amount')
        remita_mandate_id = serializer.validated_data.get('remita_mandate_id')
        payment_date = serializer.validated_data.get('payment_date')
        payment_method = serializer.validated_data.get('payment_method')

        pay_date = payment_date

        print(f"payment date :::::::::::::::: {payment_date}")

        print(
            f"\n\n\n\n ::::::::::::::::::::::::::::::: date coming for frontend {payment_date} \n\n\n\n\n")

        check_repayment = LoanRepayment.objects.filter(
            remita_mandate_id=remita_mandate_id, amount=amount, payment_date=pay_date)

        try:
            user = CustomUser.objects.get(email=request.user.email)
        except:
            data = {
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "please login before you can post repayment"
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # check if mandate is_valid
        get_manadate_date = check_mandate_branch(remita_mandate_id, phone)

        if type(get_manadate_date) == dict:
            if get_manadate_date["status"] == 400:
                data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid mandate. please reverify this mandate and post again"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            elif get_manadate_date["status"] == 200:
                if check_repayment:
                    LoanRepayment.objects.create(
                        user=user,
                        phone=phone,
                        amount=amount,
                        remita_mandate_id=remita_mandate_id,
                        payment_date=pay_date,
                        payment_method=payment_method,
                        internal=get_manadate_date["data"]["internal_branch"],
                        external=get_manadate_date["data"]["external_branch"],
                        branch_name=get_manadate_date["data"]["branch_name"],
                        is_duplicate=True,

                    )

                    data = {
                        # gives an error code stating the user phone number
                        "status": status.HTTP_302_FOUND,
                        "phone": phone,
                        "message": "This repayment transaction already exist do you want to proceed?"
                    }

                    request.session["phone"] = phone

                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    LoanRepayment.objects.create(
                        user=user,
                        phone=phone,
                        amount=amount,
                        remita_mandate_id=remita_mandate_id,
                        payment_date=payment_date,
                        payment_method=payment_method,
                        internal=get_manadate_date["data"]["internal_branch"],
                        external=get_manadate_date["data"]["external_branch"],
                        branch_name=get_manadate_date["data"]["branch_name"]
                    )

                    data = {
                        "status": status.HTTP_201_CREATED,
                        "message": "repayment created"
                    }

                    return Response(data, status=status.HTTP_201_CREATED)

        else:
            data = {
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal server error"
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = RepaymentSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class ConfirmDuplicateRepayment(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ConfirmRepaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")

        get_repayment = LoanRepayment.objects.filter(
            phone=phone, is_duplicate=True).last()

        if get_repayment:
            get_repayment.is_duplicate = False
            get_repayment.is_flagged = True
            get_repayment.save()

            data = {
                "status": status.HTTP_200_OK,
                "message": "Repayment posted successfully"
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Error finding and confirming duplicate repayment. contact the tech team"
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class Changepassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                response = {
                    'status': 'failed',
                    'code': status.HTTP_400_BAD_REQUEST,

                    'message': 'password failed',

                    'data': []
                }
                return Response(response)
            # set password hashes the password that user will get
            self.object.set_password(serializer.data.get('new_password'))

            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,

                'message': 'password updated successfully',

                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def approved_repayment(request):

    if request.method == "GET":
        approved = LoanRepayment.objects.filter(
            is_approved=True, is_mandate_closed=False, repayment_posted=False)
        serializer = RepaymentSerializer(approved, many=True)

        print(serializer.data)
        return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def pending_repayment(request):
    if request.method == "GET":
        pending = LoanRepayment.objects.filter(is_approved=False)
        data = []
        serializer = RepaymentSerializer(pending, many=True)

        print(serializer.data)

        return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Approve_one(request):
    if request.method == "POST":
        serializer = ApproveoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_designation = serializer.validated_data["is_staff"]
        payment_id = int(serializer.validated_data["payment_id"])
        is_approved = serializer.validated_data["is_approved"]
        email = serializer.validated_data["email"]
        user = CustomUser.objects.filter(
            email=email, is_staff=user_designation)
        if user:

            print(user.values())
            loan = LoanRepayment.objects.filter(
                id=payment_id).update(is_approved=is_approved)
            print(loan)
            result = LoanRepayment.objects.filter(id=payment_id)

            print(result.values())
            response = {
                'status': 'success',

                'message': 'payment approval updated'
            }
        else:
            response = {
                'status': 'unsuccessful',

                'message': 'payment approval not successful'
            }
        return Response(data=response, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Approve_all(request):
    if request.method == "POST":
        serializer = ApproveallSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_designation = serializer.validated_data["is_staff"]
        approve_all = serializer.validated_data["is_approved_all"]
        email = serializer.validated_data["email"]
        user = CustomUser.objects.filter(
            email=email, is_staff=user_designation)
        if user and approve_all:

            print(user.values())
            loan = LoanRepayment.objects.filter(
                is_approved=False).update(is_approved=True)
            print(loan)
            response = {
                'status': 'success',

                'message': 'all payment approved successfully'
            }
        else:
            response = {
                'status': 'unsuccessful',

                'message': 'you do not have permission to carry out this action'
            }
        return Response(data=response, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.email for user in CustomUser.objects.all()]
        return Response(usernames)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateApprovedPayment(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    """
        This endpoint update approved payment db after repayment have been posted to the mandates branch
    """
    serializer_class = UpdateAprrovedPaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        mandate = serializer.validated_data.get("mandate")
        phone = serializer.validated_data.get("phone")

        try:
            get_loan_repayment = LoanRepayment.objects.get(
                phone=phone, remita_mandate_id=mandate)
        except:
            get_loan_repayment = None

        if get_loan_repayment:
            get_loan_repayment.repayment_posted = True
            get_loan_repayment.save()

        data = {
            "status": status.HTTP_200_OK
        }

        return Response(data, status=status.HTTP_200_OK)
