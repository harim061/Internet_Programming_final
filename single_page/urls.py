from django.urls import path
from single_page import views

urlpatterns = [ #IP주소/
    path('',views.landing),
    path('about_me/',views.about_me),
    path('mypage/',views.mypage),
]