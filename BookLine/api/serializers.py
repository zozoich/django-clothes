from rest_framework import serializers

from demo.models import Product, Cart, Order


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'name', 'date', 'category', 'url', 'year']


class CartSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Cart
        fields = ['id', 'product', 'count']


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status_verbose')
    products = serializers.ListField(source='get_products')
    user = serializers.CharField(source='user.full_name')

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'date', 'products']