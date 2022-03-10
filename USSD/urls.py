
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('gateway.urls'))
    # path('repayment/',include('repayment.urls')),
]
