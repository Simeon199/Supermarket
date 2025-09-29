from .serializers import MarketSerializer, ProductSerializer, SellerSerializer, SellerListSerializer
from market_app.models import Market, Seller, Product
from rest_framework import mixins, generics
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass

class ProductViewSet(ListRetrieveViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class MarketDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    lookup_field = 'pk'

class SellerDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    lookup_field = 'pk'    

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

class SellerOfMarketList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
): 
    serializer_class = SellerSerializer

    def get_queryset(self):
        market_id = self.kwargs.get('market_id')
        return Seller.objects.filter(markets__id=market_id)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        market_id = self.kwargs.get('market_id')
        if market_id:
            data = request.data.copy()
            data['market_ids'] = [market_id]
            serializer = self.get_serializer(data=data)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)