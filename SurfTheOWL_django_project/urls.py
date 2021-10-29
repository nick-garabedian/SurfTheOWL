"""SurfTheOWL_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Comment by Nick: Builds the paths to the server, for communication with the server
from django.contrib import admin
from django.urls import path
from SurfTheOWL import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('landing', views.landing),
    path('', views.welcome),
    path('Surfing', views.search),
    path('download_json', views.download_search_result_json),
    path('download_duplicate_ids', views.download_du_ids),
    path('download_classes_no_id', views.download_class_no_id)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
