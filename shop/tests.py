from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.auth import get_user_model
# from PIL import Image as pil_Image
# import io

from .models import (
    Product,
    Image,
    Order,
    Shipment,
    Category,
    Cart,
    Tag,
    Review,
    Shop,
    ShopStyle,
)


User = get_user_model()


def _create_customer(
        username='test',
        password='testPass123',
        email='test@user.xyz'
    ):
    
    customer = User.objects.create(
        username=username,
        password=password,
        email=email
    )
    return customer

def _create_merchant():
    merchant = User.objects.create(
        username='mercator',
        password='testPass123',
        email='mercator@mail.com',
        account_type=User.MERCHANT
    )
    return merchant

def _create_shop(owner: User, points=0) -> Shop:
    shop = Shop.objects.create(
        owner=owner,
        points=points
    )
    return shop


class ProductTests(TestCase):
    def setUp(self):
        self.merchant = _create_merchant()
        self.shop = _create_shop(self.merchant)
        self.book_category = Category.objects.create(
            name='Books',
            description='A place to find any book you want.'
        )
        self.book_tag = Tag.objects.create(name='book')
        self.reading_tag = Tag.objects.create(name='reading')
        self.book_product = Product.objects.create(
            title='Lord of the Rings:The Fellowship of the Ring',
            description="""A meek Hobbit from the Shire and eight companions 
            set out on a journey to destroy the powerful One Ring and save 
            Middle-earth from the Dark Lord Sauron.""",
            category=self.book_category,
            price=29.99,
            quantity=75,
            shop=self.shop
        )  # Add more images to this product
        self.book_cover = Image.objects.create(
            product=self.book_product,
            # I can't load a custom image from code, yet
        )

        self.flower_product = Product.objects.create(
            title='Rose',
            description='A beautiful red rose.',
            price=3.50,
            quantity=1001,
            shop=self.shop
        )
        self.flower_photo = Image.objects.create(
            product=self.flower_product,
        )

    def test_product_title(self):
        self.assertEqual(
            self.book_product.title,
            'Lord of the Rings:The Fellowship of the Ring'
        )
        self.assertEqual(self.flower_product.title, 'Rose')

    def test_product_description(self):
        self.assertEqual(
            self.book_product.description,
            """A meek Hobbit from the Shire and eight companions 
            set out on a journey to destroy the powerful One Ring and save 
            Middle-earth from the Dark Lord Sauron."""
        )
        self.assertEqual(
            self.flower_product.description,
            'A beautiful red rose.'
        )

    def test_product_image(self):
        self.assertTrue(self.book_product.images.first().image)
        self.assertEqual(
            self.book_product.images.first().image.url,
            '/media/images/default_product.png'
        )
        self.assertTrue(self.flower_product.images.first().image)

    def test_product_price(self):
        self.assertEqual(self.book_product.price, 29.99)
        self.assertEqual(self.flower_product.price, 3.50)

    def test_product_quantity(self):
        self.assertEqual(self.book_product.quantity, 75)
        self.assertEqual(self.flower_product.quantity, 1001)

    def test_product_category(self):
        self.assertEqual(self.book_product.category.name, 'Books')
        self.assertEqual(
            self.book_product.category.description,
            'A place to find any book you want.'
        )

    def test_product_tag_add(self):
        self.assertFalse(self.book_product.tags.all())
        self.book_product.tags.add(self.book_tag, self.reading_tag)
        self.assertEqual(len(self.book_product.tags.all()), 2)

    def test_product_tag_remove(self):
        self.assertFalse(self.book_product.tags.all())
        self.book_product.tags.add(self.book_tag)
        self.assertEqual(self.book_product.tags.first().name, 'book')
        self.book_product.tags.remove(self.book_tag)
        self.assertFalse(self.book_product.tags.first())

    def test_product_shop(self):
        self.assertTrue(self.book_product.shop)
        self.assertTrue(self.flower_product.shop)
        self.assertEqual(self.book_product.shop.points, 0)
        self.assertEqual(self.book_product.shop.owner.username, 'mercator')


# This might be unnecessary but i will keep it if Image model
# needs some extentions
class ImageTests(TestCase):
    def setUp(self):
        self.merchant = _create_merchant()
        self.shop = _create_shop(self.merchant)
        self.product = Product.objects.create(
            title='LotR',
            description='Test description for Image.',
            shop=self.shop
        )

        # image_file = io.BytesIO(f'{settings.MEDIA_ROOT}/images/LotR_FotR.jpg')
        self.book_image = Image.objects.create(
            product=self.product,

            # custom image upload is giving me troubles atm, will research it

            # image=SimpleUploadedFile(
            #     name='LotR_FotR.jpg',
            #     content=open(settings.MEDIA_ROOT + '/images/LotR_FotR.jpg'),
            #     content_type='image/jpeg')

            # doesn't actually open it, throws an error
            # image=pil_Image.open(image_file)
            # image=pil_Image.open(f'{settings.MEDIA_ROOT}/images/LotR_FotR.jpg')
        )

    def test_image_product(self):
        self.assertEqual(self.book_image.product.title, 'LotR')
        self.assertEqual(self.book_image.product.quantity, 1)

    def test_image_file_upload(self):
        # default image at least works
        self.assertTrue(self.book_image.image)
        self.assertEqual(
            self.book_image.image.url,
            '/media/images/default_product.png'
        )


class OrderTests(TestCase):
    def setUp(self):
        # Create a sample user
        self.customer = _create_customer()
        self.merchant = _create_merchant()
        self.shop = _create_shop(self.merchant)
        self.item1 = Product.objects.create(
            title='Random Book',
            description='Random Book Description',
            shop=self.shop
        )
        self.item2 = Product.objects.create(
            title='Random Shirt',
            description='Random Shirt Description',
            shop=self.shop
        )
        self.order = Order.objects.create(
            customer=self.customer,
            shop=self.shop
        )

    def test_order_user(self):
        self.assertTrue(self.order.customer)
        self.assertEqual(self.order.customer.username, 'test')

    def test_order_items_add(self):
        self.order.items.add(self.item1)
        self.order.items.add(self.item2)
        self.assertEqual(self.order.items.first().title, 'Random Book')
        self.assertEqual(self.order.items.last().title, 'Random Shirt')

    def test_order_status_change(self):
        self.assertEqual(self.order.status, 'PL')  # Order.PLACED by default
        self.order.status = Order.PROCESSING
        self.assertEqual(self.order.status, 'PR')
        self.order.status = Order.COMPLETE
        self.assertEqual(self.order.status, 'CO')
        self.order.status = Order.DELIVERED
        self.assertEqual(self.order.status, 'DE')
        self.order.status = Order.CANCELED
        self.assertEqual(self.order.status, 'CA')
    
    def test_order_shop(self):
        self.assertTrue(self.order.shop)
        self.assertEqual(self.order.shop.owner.username, 'mercator')


class ShipmentTests(TestCase):
    def setUp(self):
        self.shipment = Shipment.objects.create(
            email='test@mail.com',
            first_name='John',
            last_name='Doe',
            address='1337 Leet Street',
            post_code='12345',
            state='Moon Sector 17',
            city='Alexandria',
            contact_number='+133755775577'
        )

        # helper models
        self.customer = _create_customer(username='JohnDoe')
        self.merchant = _create_merchant()
        self.shop = _create_shop(self.merchant)
        self.order = Order.objects.create(
            customer=self.customer,
            shop=self.shop
        )

    def test_shipment_email(self):
        self.assertEqual(self.shipment.email, 'test@mail.com')

    def test_shipment_names(self):
        self.assertEqual(self.shipment.first_name, 'John')
        self.assertEqual(self.shipment.last_name, 'Doe')

    def test_shipment_address(self):
        self.assertEqual(self.shipment.address, '1337 Leet Street')

    def test_shipment_post_code(self):
        self.assertEqual(self.shipment.post_code, '12345')

    def test_shipment_state(self):
        self.assertEqual(self.shipment.state, 'Moon Sector 17')

    def test_shipment_city(self):
        self.assertEqual(self.shipment.city, 'Alexandria')

    def test_shipment_contact_number(self):
        self.assertEqual(self.shipment.contact_number, '+133755775577')

    def test_shipment_method(self):
        # Shipment.MAIL by default
        self.assertEqual(self.shipment.shipping_method, 'ML')
        self.assertEqual(
            self.shipment.get_shipping_method_display(),
            'Mail'
        )

        self.shipment.shipping_method = Shipment.JEFF_BEZOS
        self.assertEqual(self.shipment.shipping_method, 'JB')
        self.assertEqual(
            self.shipment.get_shipping_method_display(),
            'Jeff Bezos with a bycicle (cheapest)')

    def test_shipment_order_add(self):
        self.shipment.order = self.order
        self.assertTrue(self.shipment.order)
        self.assertTrue(self.shipment.order.shop)
        self.assertEqual(self.shipment.order.customer.username, 'JohnDoe')


class CartTests(TestCase):
    def setUp(self):
        self.customer = _create_customer()
        self.merchant = _create_merchant()
        self.shop = _create_shop(owner=self.merchant)
        self.item1 = Product.objects.create(
            title='Smartphone',
            description='Just a regular smartphone',
            shop=self.shop
        )
        self.item2 = Product.objects.create(
            title='Flask',
            description='Pretty cool flask for water.',
            shop=self.shop
        )
        self.cart = Cart.objects.create(
            user=self.customer
        )

    def test_cart_user(self):
        self.assertTrue(self.cart.user)
        self.assertEqual(self.cart.user.username, 'test')

    def test_cart_item_add(self):
        self.assertFalse(self.cart.items.first())
        self.cart.items.add(self.item1)
        self.assertEqual(self.cart.items.first().title, 'Smartphone')
        self.assertTrue(self.cart.items.first())

    def test_cart_item_remove(self):
        self.cart.items.add(self.item1)
        self.assertTrue(self.cart.items.first())
        self.cart.items.remove(self.item1)
        self.assertFalse(self.cart.items.first())

    def test_cart_clear(self):
        self.cart.items.add(self.item1, self.item2)
        self.assertTrue(self.cart.items.all())
        self.cart.clear()
        self.assertFalse(self.cart.items.all())


class ReviewTests(TestCase):
    def setUp(self):
        self.customer = _create_customer()
        self.merchant = _create_merchant()
        self.shop = _create_shop(owner=self.merchant)
        self.product = Product.objects.create(
            title='Notebook',
            description='Regular notebook in A5 format.',
            shop=self.shop
        )
        self.review = Review.objects.create(
            product=self.product,
            user=self.customer,
            text="10/10 would buy again!"
        )

    def test_review_product_relation(self):
        self.assertTrue(self.product.reviews)
        self.assertEqual(len(self.product.reviews.all()), 1)

    def test_review_user_relation(self):
        self.assertTrue(self.customer.reviews)
        self.assertEqual(len(self.customer.reviews.all()), 1)

    def test_review_text(self):
        self.assertEqual(self.review.text, "10/10 would buy again!")


class ShopTests(TestCase):
    def setUp(self):
        self.merchant = _create_merchant()
        self.shop = _create_shop(self.merchant, points=7)

    def test_shop_owner(self):
        self.assertTrue(self.shop.owner)
        self.assertEqual(self.shop.owner.account_type, User.MERCHANT)
        self.assertEqual(self.shop.owner.username, 'mercator')

    def test_shop_points(self):
        self.assertEqual(self.shop.points, 7)


class ShopStyleTests(TestCase):
    def setUp(self):
        self.shop_style = ShopStyle.objects.create()

    def test_shop_style_logo(self):
        self.assertEqual(
            self.shop_style.logo.url,
            '/media/images/shops/shop_default_logo.png'
        )

    def test_shop_style_background_style(self):
        self.assertEqual(self.shop_style.background_style, 'C')
        self.assertEqual(
            self.shop_style.get_background_style_display(),
            'Color'
        )
        self.shop_style.background_style = ShopStyle.IMAGE
        self.assertEqual(self.shop_style.background_style, 'I')
        self.assertEqual(
            self.shop_style.get_background_style_display(),
            'Image'
        )

    def test_shop_style_theme_colors(self):
        self.assertEqual(self.shop_style.first_theme_color, '#f8f9fa')
        self.assertEqual(self.shop_style.second_theme_color, '#f6bd60')
        self.assertEqual(self.shop_style.third_theme_color, '#343a40')

        self.shop_style.first_theme_color = '#000000'
        self.assertEqual(self.shop_style.first_theme_color, '#000000')

# Analytics tests

# Visit Tests, I really don't know how this will be done
