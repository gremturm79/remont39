from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.main, name='main'),
    path('gallery/', views.gallery, name='gallery'),
    path('calculate/', views.calculate, name='calculate'),
    path('reviews/', views.reviews, name='reviews'), # страница с отображением отзывов
    path('write-review/', views.write_reviews, name='write-review'),
    path('contact/', views.contact, name='contact'),
    path('enter/', views.enter, name='enter'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('data-page/', views.data_page, name='data-page'),
    path('delete/', views.delete_user, name='delete'),
    path('add-favourite/', views.add_favourite, name='add_favourite'),
    path('favourite-images/', views.favourite_images, name='favourite_images'),
    path('remove-favourite/', views.remove_favourite, name='remove_favourite'),
    path('calculate_table/', views.calculate_table, name='calculate_table'),
    path('delete_pricing/', views.delete_pricing, name='delete_pricing'),
    path('price_list/', views.price_list, name='price_list'),
    path('found/', views.found_price_page, name='found'),
    path('view_pdf/', views.some_view, name='view_pdf'),
    path('clear/', views.clear_tag, name='clear'),
    path('calculate-apartments/', views.calculate_apartments, name='calculate-apartments'),
    path('personal_account/<str:pk>/', views.personal_account, name='personal_account'),
    path('location-objects/<str:pk>/', views.location_objects, name='location-objects'),

]

htmx_urlpatterns = [
    path('check-username/', views.check_username, name='check-username'),
    path('check-city/', views.search_city, name='check-city'),
    path('found-price/', views.found_price, name='found-price'),
    path('create-my-object/', views.create_my_object, name='create-my-object'),
    path('delete-object/', views.delete_object, name='delete-object'),
    path('delete-threed/', views.delete_threed, name='delete-threed'),
    path('send-htmx-message/', views.send_htmx_message, name='send-htmx-message'),
    path('spinner/', views.spinner, name='spinner')
]

urlpatterns += htmx_urlpatterns

# путь url для медиафайлов в режиме разработки сайта
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
