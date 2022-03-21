
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('gateway.urls')),
    # path('auth', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    # path('repayment/',include('repayment.urls')),
]