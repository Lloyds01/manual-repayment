# from django import views
from multiprocessing.managers import Namespace
from xml.etree.ElementInclude import include
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    path('login/', LoginView.as_view()),
    # path('logout/',Logout.as_view()),
    path('logout/', user_logout),
    path("repayment/", Repayment.as_view()),
    path('password/', Changepassword.as_view()),
    path("approved/", approved_repayment),
    path('pending/', pending_repayment),
    path('approve_one/', Approve_one),
    path('approve_all/', Approve_all),
    path('confirm_duplicate/', ConfirmDuplicateRepayment.as_view()),
    path('api/users/', ListUsers.as_view()),
    path('update_approved_payment/', UpdateApprovedPayment.as_view()),
    path('all_repayment/',all_repayment)

]
