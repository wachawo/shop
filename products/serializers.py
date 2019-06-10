from rest_framework import serializers
from .models import Product


class ProductShortSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    def get_category(self, product):
        return product.category.name

    def get_link(self, product):
        return "/product/%d/" % product.id

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'stock', 'link')


class ProductLongSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, product):
        return product.category.name

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'image', 'price', 'stock', 'description')
