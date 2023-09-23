from django.urls import path
from . import views

urlpatterns=[
    path('home/',views.home,name='home'),
    path('login/',views.loginPage,name="login"),
    path('register/',views.registerPage,name="register"),
    path('logout/',views.logoutPage, name='logout'),
    path('otp/',views.otp,name='otp'),
    path('process/',views.process,name='process'),
    path('generate/',views.generate,name='generate'),
    path('chat/',views.chat,name='chat')
]