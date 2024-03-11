from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

from demo import views
from demo.views import *
from BookLine import settings

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('validate_username', validate_username, name='validate_username'),
    path('validate_name', validate_name, name='validate_name'),
    path('validate_email', validate_email, name='validate_email'),
    path('validate_surname', validate_surname, name='validate_surname'),
    path('validate_patronymic', validate_patronymic, name='validate_patronymic'),

    path('oplata', oplata, name='oplata'),
    path('magaz', magaz, name='magaz'),
    path('', catalog, name='catalog'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('product/<pk>', product, name='product'),

    path('cart', cart, name='cart'),
    path('to_cart/<pk>', to_cart, name='to_cart'),
    path('minus_cart/<pk>', minus_cart, name='minus_cart'),
    path('orders', OrderListView.as_view(), name='orders'),
    path('delete_order/<pk>', delete_order, name='delete_order'),
    path('checkout', checkout, name='checkout'),



]
urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)