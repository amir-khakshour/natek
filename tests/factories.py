import factory
from decimal import Decimal as D

from goods.models import Brand, Product, Category, ProductCategory, ProductImage


class BrandFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Brand %d' % n)

    class Meta:
        model = Brand


class CategoryFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Category %d' % n)
    depth = 1  # naive handling of treebeard node fields.
    path = factory.Sequence(lambda n: '%04d' % n)

    class Meta:
        model = Category


class ProductCategoryFactory(factory.DjangoModelFactory):
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = ProductCategory


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    brand = factory.SubFactory(BrandFactory)
    title = factory.Sequence(lambda n: 'Product %d' % n)
    model = factory.Sequence(lambda n: 'Product Model %d' % n)
    categories = factory.RelatedFactory(
        'tests.factories.ProductCategoryFactory', 'product')

    price = D('9.99')
    price_currency = "EUR"


class ProductImageFactory(factory.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory, stockrecords=[])
    original = factory.django.ImageField(width=100, height=200, filename='test_image.jpg')

    class Meta:
        model = ProductImage
