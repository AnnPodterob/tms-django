"""
URL configuration for mysite project.

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
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('polls-app/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('articles-app/', include('articles.urls')),
    path('shop/', include('shop.urls')),
    path('api/', include('api.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    # path('django_pq/', include('django_pq.urls')),
]
