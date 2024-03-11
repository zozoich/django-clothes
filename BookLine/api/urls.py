from django.urls import path

from api import views
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('products', views.products),
    path('products/<int:pk>', views.product_detail),
    path('token', auth_views.obtain_auth_token),
    path('cart', views.CartList.as_view()),
    path('order', views.OrderList.as_view()),
]
