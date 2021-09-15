from django.test import TestCase
from mainapp.models import Product, Category


class ProductTestCaset(TestCase):

    def setUp(self) -> None:

        animals = Category.objects.create(name='Animals', slug='animals')
        Product.objects.create(title="Lion", slug="lion", price=13, category=animals, description='hi')


    def test_products(self):
        lion = Product.objects.get(title="Lion")
        self.assertEqual(lion.title, "Lion")
