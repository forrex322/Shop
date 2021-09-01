from django.test import TestCase
from Shop.mainapp.models import Product

class ProductTestCaset(TestCase):

    def setUp(self) -> None:
        Product.objects.create(title="Lion", slug="lion")

    def test_products(self):

        lion = Product.objects.get(title="Lion")
        self.assertEqual(lion.title, "Lion")