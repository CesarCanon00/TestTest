from django.urls import path, URLPattern, URLResolver
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('home',views.Home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('testview/<str:user>/<str:idtest>',views.testview,name='testview'),
]