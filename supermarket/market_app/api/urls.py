
from django.urls import path
from .views import MarketsView, MarketDetailView, SellersView, ProductsView, SellerDetailView, ProductDetailView, SellerOfMarketList

urlpatterns = [
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketDetailView.as_view(), name='market-detail'),
    path('market/<int:pk>/sellers/', SellerOfMarketList.as_view()),
    path('seller/', SellersView.as_view()),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name='seller-single'), # seller-detail
    path('products/', ProductsView.as_view()),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product-detail')
]