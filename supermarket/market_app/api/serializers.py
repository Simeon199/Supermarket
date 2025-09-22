from rest_framework import serializers
from market_app.models import Market, Seller, Product

class MarketSerializer(serializers.HyperlinkedModelSerializer): # ModelSerializer
     
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
     
class MarketHyperLinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer): # ModelSerializer

         def __init__(self, *args, **kwargs):

          # This line tries to remove the key 'fields' from kwargs and assign its value to fields.
          # If 'fields' is not present in kwargs, it assigns None to fields (instead of raising an error).

          fields = kwargs.pop('fields', None)

          # Instantiate the superclass normally
          super().__init__(*args, **kwargs)

          if fields is not None:
               # Drop any fields that are not specified in the `fields` argument.
               allowed = set(fields)
               existing = set(self.fields)
               # for field_name in existing - allowed:
               # Finds all fields that exist on the serializer but are not in the allowed set (i.e., fields the caller did NOT request).
               for field_name in existing - allowed:
                    self.fields.pop(field_name)
     
     # sellers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='seller_single')
     
class Meta:
     model = Market
     fields=['id', 'url', 'name', 'location', 'description', 'net_worth']
         

class SellerSerializer(serializers.ModelSerializer):
     markets = MarketSerializer(many=True, read_only=True)
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
    
class ProductSerializer(serializers.Serializer):
     id = serializers.IntegerField(read_only=True)
     name = serializers.CharField(max_length=255)
     description = serializers.CharField()
     price = serializers.DecimalField(max_digits=100, decimal_places=2)
     market = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all())
     seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())

     def create(self, validated_data):
          print(f"validated data: {validated_data['market']}")
          # market = Market.objects.get(pk=validated_data['market'])
          # seller = Seller.objects.get(pk=validated_data['seller'])
          # validated_data['market'] = market
          # validated_data['seller'] = seller
          return Product.objects.create(**validated_data)
     
     def update(self, instance, validated_data):
          # print(f"instance type: {instance}")
          instance.name = validated_data.get('name', instance.name)
          instance.description = validated_data.get('description', instance.description)
          instance.price = validated_data.get('price', instance.price)
          if 'market' in validated_data:
               instance.market = Market.objects.get(pk=validated_data['market'])
          if 'seller' in validated_data:
               instance.seller = Seller.objects.get(pk=validated_data['seller'])
          instance.save()
          return instance
     
# Seller object for test purposes

# {
#      "name": "Seller1",
#      "contact_info": "Seller1@example.com",
#      "markets": [1]
# }

# Product objects for test purposes

# {
#   "name": "Orange Juice",
#   "description": "Freshly squeezed orange juice.",
#   "price": "4.99",
#   "market": 1,
#   "seller": 1
# }