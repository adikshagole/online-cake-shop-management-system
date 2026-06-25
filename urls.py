

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('menu/', menu, name='menu'),
    path('about/', about, name='about'),
    path('customize/', customize, name='customize'),
    path('order/', order, name='order'),
    path('add/', add_item, name='add_item'),
    path('edit/<int:pk>/', edit_item, name='edit_item'),
    path('delete/<int:pk>/', delete_item, name='delete_item'),

    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),

    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('update-quantity/<int:pk>/<str:action>/', update_quantity, name='update_quantity'),
    path('remove-item/<int:pk>/', remove_item, name='remove_item'),
]