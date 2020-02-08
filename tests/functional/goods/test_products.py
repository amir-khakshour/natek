from tests.utils import APITest
from tests.factories import ProductFactory


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
