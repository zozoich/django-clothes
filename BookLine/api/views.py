from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ProductSerializer, CartSerializer, OrderSerializer
from demo.models import Product, Cart, Order, ItemInOrder


@csrf_exempt
def products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)


class BearerAuth(TokenAuthentication):
    keyword = 'Bearer'


class CartList(APIView):
    authentication_classes = [BearerAuth, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        cart_item = request.user.cart_set.all()
        serializer = CartSerializer(cart_item, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        product = Product.objects.get(pk=data['product_id'])
        item_in_cart = Cart(user=request.user, product=product, count=1)
        item_in_cart.save()
        return Response(CartSerializer(item_in_cart).data)


class OrderList(APIView):
    authentication_classes = [BearerAuth, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        order_item = request.user.order_set.all()
        serializer = OrderSerializer(order_item, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        password = data['password']
        valid = request.user.check_password(password)
        if not valid:
            return JsonResponse({
                'error': "Invalid password"
            })
        item_in_cart = request.user.cart_set.all()
        if not item_in_cart:
            return JsonResponse({
                "error": 'Empty cart'
            })
        order = Order.objects.create(user=request.user)
        for item in item_in_cart:
            ItemInOrder.objects.create(order=order, product=item.product, count=item.count,
                                       price=item.count * item.product.price)
        item_in_cart.delete()
        return JsonResponse({
            'message': "Заказ добавлен"
        })