from django.urls import path
from . import views

urlpatterns = [
    path('', views.renovation_bathroom, name='renovation_bathroom'),
    path('bathroom_gallery/', views.gallery, name='bathroom_gallery'),
    path('info-objects/', views.view_type_objects, name='info-objects'),
]