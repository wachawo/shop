from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Category, Product
from .serializers import ProductShortSerializer, ProductLongSerializer
from rest_framework.decorators import api_view


def categories(request):
    pass


@api_view(['GET'])
def products(request, category_slug=None):
    p = Product.objects.filter(stock__gt=0)
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        p = p.filter(category_id=category.id)
    context = {"products": ProductShortSerializer(p, many=True).data}
    html = render_to_string('products.html', request=request, context=context)
    return HttpResponse(html)


@api_view(['GET'])
def product(request, id):
    p = get_object_or_404(Product, pk=id)
    context = {"product": ProductLongSerializer(p, many=False).data}
    html = render_to_string('product.html', request=request, context=context)
    return HttpResponse(html)
