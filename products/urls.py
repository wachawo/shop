from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^categories/$', views.categories),
    url(r'^$', views.products),
    url(r'^products/$', views.products),
    url(r'^products/([^/]+)/$', views.products),
    url(r'^product/(\d+)/$', views.product),
]
