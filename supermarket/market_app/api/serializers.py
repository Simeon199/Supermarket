from rest_framework import serializers
from market_app.models import Market, Seller, Product

# Reusable base: allows passing `fields=['id', 'name']` at runtime to limit output

class DynamicFieldsHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
     def __init__(self, *args, **kwargs):
          fields = kwargs.pop('fields', None) # optional list/tuple of fields to keep
          super().__init__(*args, **kwargs)
          if fields is not None:
               allowed = set(fields)
               existing = set(self.fields)
               for field_name in existing - allowed:
                    self.fields.pop(field_name)

class MarketSerializer(DynamicFieldsHyperlinkedModelSerializer): # ModelSerializer
     
     sellers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='seller_single')
     
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
         

class SellerSerializer(serializers.ModelSerializer):

     # For reads: include nested markets (as MarketSerializer objects)
     markets = MarketSerializer(many=True, read_only=True)

     # For writes: accept market IDs and map them to the actual many-to-many-field via source='market'
     market_ids = serializers.PrimaryKeyRelatedField(
          queryset=Market.objects.all(),
          many=True,
          write_only=True,
          source='markets'
     )

     market_count = serializers.SerializerMethodField()

     class Meta:
          model = Seller
          fields = ["id", "name", "market_ids", "market_count", "markets", "contact_info"]

     def get_market_count(self, obj):
          return obj.markets.count()

class ProductSerializer(serializers.ModelSerializer):
     # For writes: accept FKs by ID (DRF validates and converts instances)
      market = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all())
      seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())

      class Meta:
           model = Product
           fields = ["id", "name", "description", "price", "market", "seller"]