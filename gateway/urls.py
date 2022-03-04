# from django import views
from multiprocessing.managers import Namespace
from django.urls import path,include
from .views import *

urlpatterns = [

    path('login/',LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('refresh/', RefreshView.as_view()),
    path("repayment/", Repayment.as_view()),
    path('password/', Changepassword.as_view()),
    path('secure/', Getsecuredinfo.as_view()),
    path("approved/",approved_repayment),
    path('pending/',pending_repayment),
    path('approve/',Approve_one),
    path('approve_all/',Approve_all)

]