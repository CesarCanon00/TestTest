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
    path('insert/<str:model>',views.insert,name='insert'),
    path('update/<str:model>/<str:id>',views.update,name='update'),
    path('delete/<str:model>/<str:id>',views.delete,name='delete'),
    path('results/<str:id>',views.results, name='results'),
    path('insertid/<str:model>/<str:id>',views.insertid, name='insertid'),
    path('search',views.busqueda,name= 'busqueda'),
    path('intest/<str:user>/<str:idtest>',views.intest,name= 'intest'),
    path('results/<str:user>/<str:idtest>',views.results,name= 'results'),
]