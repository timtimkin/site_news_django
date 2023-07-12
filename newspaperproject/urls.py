from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('newspaperapp.urls', namespace='newspaperapp')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
]

