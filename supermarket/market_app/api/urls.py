
from django.urls import include, path
from .views import SellerViewSet, MarketViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sellers', SellerViewSet, basename='seller')
router.register(r'markets', MarketViewSet, basename='market')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls))
]