from rest_framework import serializers
from goods.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer()

    class Meta:
        model = Product
        fields = ('date', 'channel', 'country_code', 'os', 'impressions',
                  'clicks', 'installs', 'spend', 'revenue', 'cpi')
