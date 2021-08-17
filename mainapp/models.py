from PIL import Image

from django.db import models
from django.contrib.auth import  get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class Category(models.Model):

    name = models.CharField(max_length=256, verbose_name="Name of category")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    MIN_RESOLUTION = (0, 0)
    MAX_RESOLUTION = (8000, 8000)

    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=256, verbose_name="Name of product")
    slug = models.SlugField(max_length=256)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class CartProduct(models.Model):

    user = models.ForeignKey("Customer", verbose_name="Customer", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Cart", on_delete=models.CASCADE, related_name="related_products")
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total price")

#не працює картпродукт в адмінці
    def __str__(self):
        print(self.product)
        return "Product: {} (for cart)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey("Customer", null=True, verbose_name="Owner", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name="Total price")
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)


    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Phone number", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="Address", null=True, blank=True)
    orders = models.ManyToManyField("Order", verbose_name="Orders of customer", related_name="related_customer")

    def __str__(self):
        return "Customer: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):

    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_READY = "is_ready"
    STATUS_COMPLETED = "completed"

    BUYING_TYPE_SELF = "self"
    BUYING_TYPE_DELIVERY = "delivery"

    STATUS_CHOICES = (
        (STATUS_NEW, "New order"),
        (STATUS_IN_PROGRESS, "Order in processing"),
        (STATUS_READY, "Order is ready"),
        (STATUS_COMPLETED, "Order completed")
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, "Samovuvoz"),
        (BUYING_TYPE_DELIVERY, "Delivery")
    )

    customer = models.ForeignKey(Customer, verbose_name="Customer", related_name="related_orders", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256, verbose_name="Name")
    last_name = models.CharField(max_length=256, verbose_name="Surname")
    phone = models.CharField(max_length=20, verbose_name="Phone number")
    cart = models.ForeignKey(Cart, verbose_name="Cart", on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=20, verbose_name="Address")
    status = models.CharField(max_length=100, verbose_name="Status of order", choices=STATUS_CHOICES, default=STATUS_NEW)
    baying_type = models.CharField(max_length=100, verbose_name="Type of order", choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF)
    comment = models.TextField(verbose_name="Comment for order", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Data created order")
    order_date = models.DateField(verbose_name="Data when order was geted", default=timezone.now)

    def __str__(self):
        return str(self.id)
