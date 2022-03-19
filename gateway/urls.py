# from django import views
from multiprocessing.managers import Namespace
from xml.etree.ElementInclude import include
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    path('login/', LoginView.as_view()),
    path('log/',obtain_auth_token, name='login'),
    # path('register/', RegisterView.as_view()),
    path('refresh/', RefreshView.as_view()),
    path("repayment/", Repayment.as_view()),
    path('password/', Changepassword.as_view()),
    path('secure/', Getsecuredinfo.as_view()),
    path("approved/", approved_repayment),
    path('pending/', pending_repayment),
    path('approve_one/', Approve_one),
    path('approve_all/', Approve_all),
    path('confirm_duplicate/', ConfirmDuplicateRepayment.as_view())

]
