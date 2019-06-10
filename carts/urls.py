from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cart/$', views.cart_products),
    url(r'^cart/product/$', views.cart_product),
    url(r'^invoice/$', views.invoice),
]
