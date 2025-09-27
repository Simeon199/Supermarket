from .serializers import MarketSerializer, ProductSerializer, SellerSerializer
from market_app.models import Market, Seller, Product
from rest_framework import mixins
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class MarketsView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
    ):
    
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class SellersView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ProductsView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
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

class SellerOfMarketList(generics.ListAPIView):
    serializer_class = SellerSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk=pk)
        return market.sellers.all()