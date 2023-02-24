from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    # path('main', views.main, name='main'),
    path('main', views.responsiveWebMain, name='main'),
    path('main2', views.main2, name='main2'),
    path('recommend', views.recommend, name='recommend'),
    path('place_submit', views.submit, name='submit'),
    path('preprocessing', views.preprocessing, name='preprocessing'),
]
