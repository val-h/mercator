from django.db import models
from django.contrib.auth import get_user_model
# from .signals import object_viewed


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Tag(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Images will be a sequence of sepаrate models
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='products'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='products'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    # Specifications -> table like representation
    times_bought = models.IntegerField(default=0)
    shop = models.ForeignKey(
        'Shop',
        on_delete=models.CASCADE,
        related_name='products'
    )

    # Utils
    CONFIGURABLE_FIELDS = ['price', 'quantity', 'description', 'title']

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.title)

    def visited(self):
        Visit.objects.create(
            shop_analytics=self.shop.analytics,
            model=Visit.PRODUCT,
            model_id=self.id
        )

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category,
            'shop': self.shop.serialize(),
            'times_bought': self.times_bought
        }

    def serialize_for_user(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'category': self.category
        }


# To be used only with the Product model
class Image(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name='images')
    image = models.ImageField(
        upload_to='images/',
        default='images/default_product.png')

    def __str__(self):
        return f'{self.product.title}\'s image'


class Order(models.Model):
    items = models.ManyToManyField(
        Product,
        blank=True,
        related_name='all_orders'
    )

    PLACED = 'PL'
    CANCELED = 'CA'
    PROCESSING = 'PR'
    COMPLETE = 'CO'
    DELIVERED = 'DE'
    ORDER_OPTIONS = [
        (PLACED, 'Active'),
        (CANCELED, 'Canceled'),
        (PROCESSING, 'Processing'),
        (COMPLETE, 'Complete'),
        (DELIVERED, 'Delivered')
    ]
    status = models.CharField(
        max_length=2,
        choices=ORDER_OPTIONS,
        default=PLACED
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        default=None,
        related_name='orders'
    )
    shop = models.ForeignKey(
        'Shop',
        on_delete=models.DO_NOTHING,
        related_name='orders'
    )

    CONFIGURABLE_FIELDS = ['status', 'items']

    def __str__(self):
        return f'ID: {self.id}, Customer: {self.customer}'

    def serialize(self):
        return {
            'id': self.id,
            'status': self.status,
            'shop': self.shop.serialize(),
            'customer': self.customer.serialize(),
            'date_ordered': self.date_ordered,
            'items': [product.serialize() for product in self.items.all()]
        }

    def serialize_for_user(self):
        return {
            'id': self.id,
            'status': self.status,
            'date_ordered': self.date_ordered,
            'items': [
                product.serialize_for_user() for product in self.items.all()
            ]
        }


class Shipment(models.Model):
    # Possibly move to Foreign, orders may have more than 1 shipment
    order = models.OneToOneField(
        Order,
        on_delete=models.DO_NOTHING,
        default=None,
        null=True,
        blank=True,
        related_name='shipment'
    )
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    company = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=120)
    post_code = models.CharField(max_length=120)
    state = models.CharField(max_length=80)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=40)
    # No RegEx or library for handling phone numbers
    # Add some basic validators and stripping of white spaces
    contact_number = models.CharField(max_length=20)

    MAIL = 'ML'
    PARCEL_DELIVERY = 'PD'
    JEFF_BEZOS = 'JB'
    SHIPPING_METHODS = [
        (MAIL, 'Mail'),
        (PARCEL_DELIVERY, 'Parcel Delivery Company'),
        (JEFF_BEZOS, 'Jeff Bezos with a bиcicle (cheapest)')
    ]
    shipping_method = models.CharField(
        max_length=2,
        choices=SHIPPING_METHODS,
        default=MAIL
    )

    CONFIGURABLE_FIELDS = [
        'company',
        'address',
        'post_code',
        'stete',
        'city',
        'country',
    ]

    def __str__(self):
        return f'ID: {self.id}, Order: {self.order}'

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company': self.company,
            'address': self.address,
            'post_code': self.post_code,
            'state': self.state,
            'city': self.city,
            'contact_number': self.contact_number,
            'order': self.order.serialize()
        }

    def serialize_for_user(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company': self.company,
            'address': self.address,
            'post_code': self.post_code,
            'state': self.state,
            'city': self.city,
            'contact_number': self.contact_number,
            'order': self.order.serialize_for_user()
        }


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        related_name='cart'
    )
    items = models.ManyToManyField(
        Product,
        blank=True,
        related_name='in_carts'
    )

    def clear(self):
        self.items.clear()

    def __str__(self):
        return f'{self.user}\'s Cart'

    def serialize(self):
        return {
            'items': [item.serialize_for_user() for item in self.items.all()]
        }


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='reviews'
    )
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    CONFIGURABLE_FIELDS = ['text']

    def __str__(self):
        return f'Review on {self.product} by {self.user}'

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'text': self.text,
            'product_id': self.product.id,
            'user': {
                'id': self.user.id,
                'username': self.user.username
                # possibly add if the user had purchased this product
                # or make it that only users liek that can review
            }
        }


class Visit(models.Model):
    """
    Helper model for the analytics of every shop.

    Provides just the basic
    """
    date = models.DateTimeField(auto_now_add=True)
    shop_analytics = models.ForeignKey(
        'ShopAnalytics',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='visits'
    )

    # GenericForeignKey and ContentType are things that exist
    # For future projects, look them up
    PRODUCT = 'P'
    SHOP = 'S'
    MODEL_CHOICES = [
        (PRODUCT, 'Product'),
        (SHOP, 'Shop')
    ]
    model = models.CharField(max_length=1, choices=MODEL_CHOICES)
    model_id = models.IntegerField()


class ShopAnalytics(models.Model):
    total_products_sold = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)

    CONFIGURABLE_FIELDS = []

    # Just a temporary showcase solution
    def shop_visits(self):
        query = self.visits.filter(model=Visit.SHOP)
        return query

    def product_visits(self, id=None):
        if not id:
            query = self.visits.filter(model=Visit.PRODUCT)
        elif id:
            query = self.visits.filter(model=Visit.PRODUCT, model_id=id)
        return query

    def __str__(self):
        return f'{self.shop} - analytics'

    def serialize(self):
        return {
            'total_products_sold': self.total_products_sold,
            'total_orders': self.total_orders,
            'total_shop_visits': self.shop_visits().count(),
            'total_product_visits': self.product_visits().count()
        }

    def serialize_single_product(self, product_id):
        return {
            'product_visits': self.product_visits(product_id).count()
        }


class ShopStyle(models.Model):
    logo = models.ImageField(
        upload_to='images/shops/',
        blank=True,
        default='images/shops/shop_default_logo.png')

    COLOR = 'C'
    IMAGE = 'I'
    # GIF = 'G' ^ goes into image
    BACKGROUND_STYLES = [
        (COLOR, 'Color'),
        (IMAGE, 'Image'),
        # (GIF, 'Gif')
    ]
    background_style = models.CharField(
        max_length=1,
        choices=BACKGROUND_STYLES,
        default=COLOR
    )

    # Create custom field that validates for colors in rgb format
    first_theme_color = models.CharField(max_length=7, default='#f8f9fa')
    second_theme_color = models.CharField(max_length=7, default='#f6bd60')
    third_theme_color = models.CharField(max_length=7, default='#343a40')

    background_color = models.CharField(max_length=7, default='#000000')
    background_image = models.ImageField(
        upload_to='images/shops/',
        blank=True,
        default=None
    )

    CONFIGURABLE_FIELDS = [
        'logo',
        'background_style',
        'first_theme_color',
        'second_theme_color',
        'third_theme_color',
        'background_color',
        'background_image'
    ]

    def __str__(self):
        return f'{self.shop} - style'

    def serialize(self):
        data = {
            'logo': self.logo.url,
            'background_style': self.background_style,
            'first_theme_color': self.first_theme_color,
            'second_theme_color': self.second_theme_color,
            'third_theme_color': self.third_theme_color,
            'background_color': self.background_color
        }
        if self.background_image:
            data['background_image'] = self.background_image.url
        return data


class Shop(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='shop'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    # Will be used for marketing
    points = models.IntegerField(default=0)

    style = models.OneToOneField(
        ShopStyle,
        on_delete=models.DO_NOTHING,
        null=True,
        default=None
    )
    analytics = models.OneToOneField(
        ShopAnalytics,
        on_delete=models.DO_NOTHING,
        null=True,
        default=None
    )

    # Utils
    # Specify the fields that can be configured from the api
    CONFIGURABLE_FIELDS = ['points']

    def __str__(self):
        return f'{self.owner}\'s shop'

    def visited(self):
        Visit.objects.create(
            shop_analytics=self.analytics,
            model=Visit.SHOP,
            model_id=self.id
        )

    def serialize(self):
        return {
            'id': self.id,
            'owner': self.owner.username,
            'date_created': self.date_created,
            'points': self.points,
        }
