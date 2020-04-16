"""InsaneDjangoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from InsaneDjangoApp import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset',),
    path('admin/password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done',),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm',),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete',),
    path('',auth_views.LoginView.as_view(template_name='registration/login_staff.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('sales/',include('SalesApp.urls',namespace='SalesApp')),
    path('operations/', include('OperationsApp.urls',namespace='OperationsApp')),
    path('accounts/',include('AccountsApp.urls',namespace='AccountsApp')),
    path('dashboard/',main_views.DashboardView,name='dashboard'),
    path('403/',TemplateView.as_view(template_name='error_page_403.html'),name='error403'),
    ]
