from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework.decorators import api_view
from .models import Cart, Invoice
from products.models import Product
import json


@csrf_exempt
@api_view(['POST', 'DELETE'])
def cart_product(request):
    if request.method == 'POST':
        product_id = request.POST.get("product_id")
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return HttpResponse("Product not found.", status=400)
        count = request.POST.get("count")
        product_count = int(count) if count is not None and count.isdigit() else 1
        cart, created = Cart.objects.get_or_create(id=request.COOKIES.get('CART_ID'))
        products = json.loads(cart.products)
        if product_id not in products:
            products.update({product_id: product_count})
        else:
            products[product_id] += product_count
        if products[product_id] > product.stock:
            response = HttpResponse("Not enough products.", status=400)
        else:
            cart.products = json.dumps(products)
            cart.save()
            prices = {str(p.id): p.price for p in Product.objects.filter(pk__in=[int(p_id) for p_id in products.keys()])}
            cart_sum = sum([products[p_id] * prices[p_id] for p_id in products])
            response = HttpResponse(cart_sum)
            response.set_cookie('CART_SUM', cart_sum)
        if created:
            response.set_cookie('CART_ID', cart.id)
        return response

    if request.method == 'DELETE':
        product_id = request.POST.get("product_id")
        try:
            cart = Cart.objects.get(id=request.COOKIES.get('CART_ID'))
        except Cart.DoesNotExist:
            return HttpResponse("Cart not found.", status=400)
        products = json.loads(cart.products)
        if product_id not in products:
            return HttpResponse("Product not in cart.", status=400)
        else:
            del products[product_id]
            cart.products = json.dumps(products)
            cart.save()
            prices = {str(p.id): p.price for p in Product.objects.filter(pk__in=[int(p_id) for p_id in products.keys()])}
            cart_sum = sum([products[p_id] * prices[p_id] for p_id in products])
            response = HttpResponse(cart_sum)
            response.set_cookie('CART_SUM', cart_sum)
            return response


@api_view(['GET'])
def cart_products(request):
    response = HttpResponse()
    try:
        cart = Cart.objects.get(id=request.COOKIES.get('CART_ID'))
    except Cart.DoesNotExist:
        cart = Cart.objects.create()
        response.set_cookie('CART_ID', cart.id)
    context = {"products": [], "count": 0, "amount": 0}
    for p, c in cart.get_products().items():
        context["products"].append({
            "id": p.id,
            "link": "/product/%d/" % p.id,
            "name": p.name,
            "price": p.price,
            "count": c,
            "amount": p.price * c
        })
        context["count"] += c
        context["amount"] += p.price * c
    response.write(render_to_string('cart.html', request=request, context=context))
    return response


@csrf_exempt
@api_view(['GET', 'POST'])
def invoice(request):
    if request.method == 'GET':
        response = HttpResponse()
        try:
            cart = Cart.objects.get(id=request.COOKIES.get('CART_ID'))
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
            response.set_cookie('CART_ID', cart.id)
        context = {"products": [], "count": 0, "amount": 0}
        for p, c in cart.get_products().items():
            context["products"].append({
                "id": p.id,
                "link": "/product/%d/" % p.id,
                "name": p.name,
                "price": p.price,
                "count": c,
                "amount": p.price * c
            })
            context["count"] += c
            context["amount"] += p.price * c
        response.write(render_to_string('invoice.html', request=request, context=context))
        return response

    if request.method == 'POST':
        response = HttpResponse()
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        amount = 0
        with transaction.atomic():
            cart = Cart.objects.get(id=request.COOKIES.get('CART_ID'))
            for p, c in cart.get_products().items():
                amount += p.price * c
                p.stock -= c
                p.save()
            invoice = Invoice.objects.create(products=cart.products, name=name, phone=phone, amount=amount)
            cart.products = {}
            cart.save()
            response.write(invoice.id)
            response.set_cookie('CART_SUM', 0)
        return response
