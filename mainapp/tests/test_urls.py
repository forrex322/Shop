from decimal import Decimal

from django.test import SimpleTestCase, Client, TransactionTestCase, TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, resolve
from mainapp.models import Product, Customer, Cart, CartProduct, Category, Order
from mainapp.views import (
    ProductDetailView,
    BaseView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    CheckoutView,
    MakeOrderView,
    CategoryDetailView,
    LoginView,
    RegistrationView,
    ProfileView

)

# для того щоб тести запустились я удалив файл __init__.py з папки mainapp

#TODO: дописати тести

User = get_user_model()

class TestUrls(TestCase):

    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='password')
        category = Category.objects.create(name='Notebooks', slug='notebooks')
        image = SimpleUploadedFile("notebook_image.jpg", content=b'', content_type="image/jpg")
        product = Product.objects.create(category=category, title='Macbook', slug='macbook', description='hi', price=Decimal('1200.00'), image=image)
        customer = Customer.objects.create(user=user, phone='123', address='123')
        cart = Cart.objects.create(owner=customer)
        cart_product = CartProduct.objects.create(user=cart.owner, product=product, cart=cart)
        order = Order.objects.create(customer=customer, first_name='Dima', last_name='Andr', phone='123', cart=cart, address='123')



    def test_base_url_is_resolves(self):
        url = reverse('base')
        print(resolve(url))
        print(BaseView.as_view())
        self.assertEquals(resolve(url).func.view_class, BaseView)

    def test_product_detail_url_is_resolves(self):
        response = self.client.get('/products/macbook/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['object'].__str__(), "Macbook")

    def test_category_detail_url_is_resolves(self):
        response = self.client.get('/category/notebooks/')
        self.assertEquals(response.status_code, 200)

    def test_cart_url_is_resolves(self):
        url = reverse('cart')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, CartView)

    # def test_add_to_cart_url_is_resolves(self):
    #     response = self.client.get('/add-to-cart/macbook/')
    #     # self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, '/cart/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    # def test_delete_from_cart_url_is_resolves(self):
    #     url = reverse('delete_from_cart')
    #     print(resolve(url))
    #     self.assertEquals(resolve(url).func.view_class, DeleteFromCartView)

    # def test_change_qty_url_is_resolves(self):
    #     # url = reverse('change_qty')
    #
    #     response = self.client.post('/change-qty/macbook/')
    #     print(" /// ")
    #     print(response)
    #     print(" /// ")
    #     self.assertEquals(response.status_code, 301)

        # print(resolve(url))
        # self.assertEquals(resolve(url).func.view_class, ChangeQTYView)

    def test_checkout_url_is_resolves(self):
        url = reverse('checkout')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, CheckoutView)

    def test_make_order_url_is_resolves(self):
        url = reverse('make_order')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, MakeOrderView)

    def test_login_url_is_resolves(self):
        url = reverse('login')
        print(resolve(url))
        print(BaseView.as_view())
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_registration_url_is_resolves(self):
        url = reverse('registration')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, RegistrationView)

    def test_profile_url_is_resolves(self):
        url = reverse('profile')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ProfileView)

