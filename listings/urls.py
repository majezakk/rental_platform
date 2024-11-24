from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
    path('create/', views.listing_create, name='listing_create'),
    path('<int:pk>/edit/', views.listing_edit, name='listing_edit'),
    path('<int:pk>/delete/', views.listing_delete, name='listing_delete'),

    path('bookings/create/<int:pk>/', views.create_booking, name='create_booking'),
    path('bookings/tenant/', views.booking_list_tenant, name='booking_list_tenant'),
    path('bookings/landlord/', views.booking_list_landlord, name='booking_list_landlord'),

    path('bookings/manage/<int:pk>/<str:action>/', views.manage_booking, name='manage_booking'),

]