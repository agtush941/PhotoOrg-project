from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('login/',views.loginUser,name = 'login'),
    path('logout/',views.logoutUser,name = 'logout'),
    path('register/',views.registerUser,name = 'register'),
    path('',views.gallery,name = 'gallery'),
    path('photos/<str:pk>/',views.viewPhoto,name = 'Photo'),
    path('add/',views.addPhoto,name = 'add'),
    path('deletephoto/<str:pk>/',views.deletePhoto,name = 'deletephoto'),

]