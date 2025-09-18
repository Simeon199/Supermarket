from rest_framework import serializers
from market_app.models import Market, Seller, Product

def validate_no_x(value):
        errors = []
        if 'X' in value:
            errors.append('no X in location')
        if 'Y' in value:
             errors.append('no Y in location')
        if errors:
             raise serializers.ValidationError(errors)
        return value

class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, validators=[validate_no_x])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    def create(self, validated_data):
        return Market.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance
    
class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = MarketSerializer(many=True, read_only=True)
    # markets = serializers.StringRelatedField(many=True)

class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    # def validate_markets(self, value):
    #      markets = Market.objects.filter(id__in=value)
    #      if len(markets) != len(value):
    #           serializer = MarketSerializer(markets, many=True)
    #           raise serializers.ValidationError(serializer.data)
    #      return value

    def validate_markets(self, value):
         markets = Market.objects.filter(id__in=value)
         if len(markets) != len(value):
              raise serializers.ValidationError({"message": "passt halt nicht mit den ids"})
         return value
    
    def create(self, validated_data):
         market_ids=validated_data.pop('markets')
         seller = Seller.objects.create(**validated_data)
         markets = Market.objects.filter(id__in=market_ids)
         seller.markets.set(markets)
         return seller
    
class ProductSerializer(serializers.Serializer):
     id = serializers.IntegerField(read_only=True)
     name = serializers.CharField(max_length=255)
     description = serializers.CharField()
     price = serializers.DecimalField(max_digits=100, decimal_places=2)
     market = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all())
     seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())
     # market = serializers.IntegerField()
     # seller = serializers.IntegerField()

     def create(self, validated_data):
          # Fetch related objects using the provided IDs
          market = Market.objects.get(pk=validated_data['market'])
          seller = Seller.objects.get(pk=validated_data['seller'])
          # Remove IDs from validated_data and add actual objects
          validated_data['market'] = market
          validated_data['seller'] = seller
          return Product.objects.create(**validated_data)
     
     def update(self, instance, validated_data):
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
#   "name": "Apple Juice",
#   "description": "Freshly squeezed apple juice.",
#   "price": "3.99",
#   "market": 1,
#   "seller": 1
# }