from django.urls import path
from . import views

urlpatterns = [
    path('', views.responsiveWebMain, name='main'),
    # path('main', views.main, name='main'),
    #path('main', views.responsiveWebMain, name='main'),
    path('recommend', views.recommend, name='recommend'),
    path('place_submit', views.submit, name='submit'),
    path('preprocessing', views.preprocessing, name='preprocessing'),
    path('administrator', views.admin, name='admin'),
    path('update', views.update, name='update'),
    path('QandA', views.QandA, name='QandA'),
    path('txtCorrection', views.txtCorrection, name='txtCorrection'),
    path('coordinateCorrection', views.coordinateCorrection, name='coordinateCorrection'),
    path('date', views.date, name='date'),
    path('building_preprocessing', views.building_preprocessing, name='building_preprocessing'),
    path('XtoX_preprocessing', views.XtoX_preprocessing, name='XtoX_preprocessing'),
]
