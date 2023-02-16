from django.urls import path
from . import views

app_name= 'imagediff'

urlpatterns = [
    path('top/',          views.view_top,    name='top'),
    path('camera/',       views.view_camera, name='camera'),
    path('camera_1send/', views.view_camera_1send, name='camera_1send'),
    path('result/',       views.view_result, name='result'),
    path('config/',       views.view_config, name='config'),
    path('alert/',        views.view_alert,  name='alert'),
    path('alert/csv/',    views.view_csv,    name='csv'),
    path('word/',         views.view_word,  name='word'),
    path('log/',          views.view_log,    name='log'),
    # path('alert/add/', views.alert_add, name='alert_add'),
    # path('alert/edit/', views.alert_edit, name='alert_edit'),
    # path('alert/del/', views.alert_del, name='alert_del'),
    # path('alert/ref/', views.alert_ref, name='alert_ref'),
]