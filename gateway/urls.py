# from django import views
from multiprocessing.managers import Namespace
from django.urls import path
from .views import *

urlpatterns = [

    path('login/', LoginView.as_view()),
    # path('register/', RegisterView.as_view()),
    path('refresh/', RefreshView.as_view()),
    path("repayment/", Repayment.as_view()),
    path('password/', Changepassword.as_view()),
    path('secure/', Getsecuredinfo.as_view()),
    path("approved/", approved_repayment),
    path('pending/', pending_repayment),
    path('approve_one/', Approve_one),
    path('approve_all/', Approve_all),
    path('confirm_duplicate/', ConfirmDuplicateRepayment.as_view()),
    path('api/users/', ListUsers.as_view()),

]
