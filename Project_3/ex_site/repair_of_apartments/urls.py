from django.urls import path
from . import views

urlpatterns = [
    path('', views.repair_of_apartments, name='repair_of_apartments'),
    path('apartment_gallery/', views.apartment_gallery, name='apartment_gallery'),
    path('info-objects/', views.view_type_objects, name='info-objects_apart'),

]