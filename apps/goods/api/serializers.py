from rest_framework import serializers
from rest_framework.relations import ManyRelatedField
from django.contrib.auth import get_user_model

from ..models import Category, Brand, Product, ProductImage
from ..drf.serializers import VersionableHyperlinkedIdentityField
from ..drf.fields import CategoryField


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    breadcrumbs = serializers.CharField(source="full_name", read_only=True)
    url = VersionableHyperlinkedIdentityField(view_name="api_goods:category-products")

    class Meta:
        model = Category
        exclude = ("path", "depth", "numchild")


class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        write_only=True, required=False, queryset=Product.objects
    )

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing all products.
    TODO: provide a summary version for product lists - probably using `drf-dynamic-fields` app
    """
    images = ProductImageSerializer(read_only=True)
    url = VersionableHyperlinkedIdentityField(view_name="api_goods:product-detail")
    created_by = ProductOwnerSerializer(read_only=True)
    categories = CategoryField(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for Writing a product.
    """
    class Meta:
        model = Product
        exclude = ('date_created', 'date_updated')


class ProductTestSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing all products in test environment.
    """

    class Meta:
        model = Product
        exclude = ('date_created', 'date_updated', 'id')
