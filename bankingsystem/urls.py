from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('banking.urls')),   # include your app's URLs here
    path('api-auth/', include('rest_framework.urls')),
]
