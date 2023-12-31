"""
URL configuration for mobileapplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from mobile import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mobiles/all',views.MobileListView.as_view(),name="mobile-all"),
    #for ids urls must be in the below format
    path('mobiledetails/<int:pk>',views.MobileDetailsbyidView.as_view(),name="mobile_detailsbyid"),
    path('mobiles/<int:pk>/remove',views.MobileDelete.as_view(),name="mobile-remove"),
    path('mobiles/create',views.MobileCreateView.as_view(),name="mobile-add"),
    path('mobile/<int:pk>/update',views.MobileUpdateView.as_view(),name="mobile-update"),
    path('register',views.SignUpView.as_view(),name="register"),
    path('',views.SignInView.as_view(),name="signin"),#on localhost8000 login page come
    path('logout',views.SignOutView.as_view(),name="signout"),
    path('api/',include("api.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
