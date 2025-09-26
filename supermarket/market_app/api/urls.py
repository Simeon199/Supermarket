
from django.urls import path
from .views import markets_view, market_single_view, sellers_view, products_view, sellers_single_view, product_detail_view

urlpatterns = [
    path('market/', markets_view),
    path('market/<int:pk>/', market_single_view, name='market-detail'),
    path('seller/', sellers_view),
    path('seller/<int:pk>/', sellers_single_view, name='seller-single'),
    path('products/', products_view),
    path('products/<int:pk>', product_detail_view, name='product-detail')
]