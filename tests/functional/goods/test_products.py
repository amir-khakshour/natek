import mock
from tests.utils import APITest
from tests.factories import ProductFactory
from goods.api.serializers import ProductReadSerializer, ProductWriteSerializer, ProductTestSerializer
from django.test.client import RequestFactory


class ProductTest(APITest):
    def setUp(self):
        super().setUp()
        self.num_products = 4
        self.product_list = [ProductFactory() for _ in range(self.num_products)]

    def test_product_list(self):
        "Check if we get a list of products with the default attributes"
        self.response = self.get("api_goods:product-list")
        self.response.assertStatusEqual(200)
        # we should have four products
        self.assertEqual(len(self.response.body), self.num_products)

    def test_product_details(self):
        # fetch data
        self.response = self.get("api_goods:product-list")

        # load product data
        products = self.response.json()
        first_product = products[0]

        product_detail_fields = ProductReadSerializer().get_fields().keys()
        # verify all the fields are rendered in the list view
        for field in product_detail_fields:
            self.assertIn(field, first_product)

    def test_product_create(self):
        base_product = self.product_list[0]
        rf = self.client
        rf.force_login(self.staff_user)
        rf.version = 1  # todo add proper mocking utility to add version

        serializer = ProductWriteSerializer(base_product, context={'request': rf})
        self.response = self.post("api_goods:product-list", data=serializer.data)
        self.response.assertStatusEqual(201)  # created product
