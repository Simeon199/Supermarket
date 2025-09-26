from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, ProductSerializer, SellerSerializer
from django.shortcuts import get_object_or_404
from market_app.models import Market, Seller, Product

@api_view(['GET', 'POST'])
def markets_view(request):
    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketSerializer(
            markets, 
            many=True, 
            context={'request': request},
            fields=('id', 'name', 'net_worth')
        )
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MarketSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def market_single_view(request, pk):
    market = get_object_or_404(Market, pk=pk)
    if request.method == 'GET':
        serializer = MarketSerializer(
            market, 
            context={'request': request}
        )
        return Response(serializer.data)
    if request.method in ['PUT', 'PATCH']:
        serializer = MarketSerializer(
            market,
            context={'request': request}, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        market.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def sellers_view(request):
    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerSerializer(
            sellers, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SellerSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def sellers_single_view(request, pk):
    seller = get_object_or_404(Seller, pk=pk)
    if request.method == 'GET':
        serializer = SellerSerializer(
            seller, 
            context={'request': request}
        )
        return Response(serializer.data)
    if request.method in ['PUT', 'PATCH']:
        serializer = SellerSerializer(
            seller, 
            context={'request': request}, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(
            products, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ProductSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(
            product, 
            context={'request': request}
        )
        return Response(serializer.data)
    if request.method in ['PUT', 'PATCH']:
        serializer = ProductSerializer(
            product, 
            context={'request': request}, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)