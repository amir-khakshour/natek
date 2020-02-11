from tests.utils import APITest
from tests.factories import CategoryFactory
from goods.models import Product


class CategoryTest(APITest):
    def setUp(self):
        super().setUp()
        self.num_categories = 4
        self.category_list = [CategoryFactory() for _ in range(self.num_categories)]

    def test_category_list(self):
        self.response = self.get("api_goods:category-list")
        self.response.assertStatusEqual(200)
        self.assertEqual(len(self.response.body), self.num_categories)

    def test_product_in_category(self):
        base_category = self.category_list[0]
        self.response = self.get("api_goods:category-products", url_kwargs={'pk': base_category.pk})
        self.response.assertStatusEqual(200)

    def test_total_product_in_category(self):
        base_category = self.category_list[0]
        self.response = self.get("api_goods:category-products", url_kwargs={'pk': base_category.pk})
        num_products_in_category = Product.objects.filter(categories__id=base_category.pk).count()
        self.assertEqual(len(self.response.body), num_products_in_category)
