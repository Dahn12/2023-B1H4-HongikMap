from django.urls import path

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('map', views.map,name = 'map' )
]
