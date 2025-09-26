from rest_framework import serializers
from market_app.models import Market, Seller, Product

# Reusable base: allows passing `fields=['id', 'name']` at runtime to limit output

class DynamicFieldsHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
     def __init__(self, *args, **kwargs):
          fields = kwargs.pop('fields', None) 
          super().__init__(*args, **kwargs)
          if fields is not None:
               allowed = set(fields) # fields = ('id', 'name', 'net_worth')
               existing = set(self.fields) # self.fields = ('id', 'name', 'location', 'description', 'net_worth')
               for field_name in existing - allowed:
                    self.fields.pop(field_name)

class MarketSerializer(DynamicFieldsHyperlinkedModelSerializer): # ModelSerializer
     url = serializers.HyperlinkedIdentityField(view_name='market-detail')
     sellers = serializers.HyperlinkedRelatedField(
          many=True, 
          read_only=True,
          view_name='seller-single'
     )
     
     class Meta:
         model = Market
         fields = '__all__'
         
     def validate_name(self, value):
        errors = []
        if 'X' in value:
            errors.append('no X in location')
        if 'Y' in value:
             errors.append('no Y in location')
        if errors:
             raise serializers.ValidationError(errors)
        return value 
         
class SellerSerializer(DynamicFieldsHyperlinkedModelSerializer):
     url = serializers.HyperlinkedIdentityField(view_name='seller-single') # seller-detail
     markets = serializers.HyperlinkedRelatedField(
          many=True,
          read_only=True,
          view_name='market-detail'
     )
     market_count = serializers.SerializerMethodField()
     
     def get_market_count(self, obj):
          return obj.markets.count()
     
     class Meta:
          model = Seller
          fields = [
               "url", 
               "id", 
               "name", 
               "market_count", 
               "markets", 
               "contact_info"
          ] # "market_ids"

class ProductSerializer(DynamicFieldsHyperlinkedModelSerializer):
     url = serializers.HyperlinkedIdentityField(view_name='product-detail')
     market = serializers.HyperlinkedRelatedField(
          queryset=Market.objects.all(), view_name='market-detail'
     )
     seller = serializers.HyperlinkedRelatedField(
          queryset=Seller.objects.all(), view_name='seller-single'
     )
     class Meta:
          model = Product
          fields = [
               "url", 
               "id", 
               "name", 
               "description", 
               "price", 
               "market", 
               "seller"
          ]