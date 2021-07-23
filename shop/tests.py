from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.auth import get_user_model
# from PIL import Image as pil_Image
# import io

from .models import Product, Image, Order, Shipment, Category


User = get_user_model()


class ProductTests(TestCase):
    def setUp(self):
        self.book_category = Category.objects.create(
            name='Books',
            description='A place to find any book you want.'
        )
        self.book_product = Product.objects.create(
            title='Lord of the Rings:The Fellowship of the Ring',
            description="""A meek Hobbit from the Shire and eight companions 
            set out on a journey to destroy the powerful One Ring and save 
            Middle-earth from the Dark Lord Sauron.""",
            category=self.book_category,
            price=29.99,
            quantity=75
        ) # Add more images to this product
        self.book_cover = Image.objects.create(
            product=self.book_product,
            # I can't load a custom image from code, yet
        )

        self.flower_product = Product.objects.create(
            title='Rose',
            description='A beautiful red rose.',
            price=3.50,
            quantity=1001
        )
        self.flower_photo = Image.objects.create(
            product=self.flower_product,
        )
    
    def test_product_title(self):
        self.assertEqual(
            self.book_product.title,
            'Lord of the Rings:The Fellowship of the Ring')
        self.assertEqual(self.flower_product.title, 'Rose')

    def test_product_description(self):
        self.assertEqual(
            self.book_product.description,
            """A meek Hobbit from the Shire and eight companions 
            set out on a journey to destroy the powerful One Ring and save 
            Middle-earth from the Dark Lord Sauron.""")
        self.assertEqual(
            self.flower_product.description,
            'A beautiful red rose.')

    def test_product_image(self):
        self.assertTrue(self.book_product.images.first().image)
        self.assertEqual(
            self.book_product.images.first().image.url,
            '/media/images/default_product.png')
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
            'A place to find any book you want.')


# This might be unnecessary but i will keep it if Image model
# needs some extentions
class ImageTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title='LotR',
            description='Test description for Image.',
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
            '/media/images/default_product.png')


class OrderTests(TestCase):
    def setUp(self):
        # Create a sample user
        self.customer = User.objects.create(
            username='test',
            password='testPass123',
            email='test@user.xyz'
        )
        self.item1 = Product.objects.create(
            title='Random Book',
            description='Random Book Description'
        )
        self.item2 = Product.objects.create(
            title='Random Shirt',
            description='Random Shirt Description'
        )
        self.order = Order.objects.create(
            customer=self.customer,
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
        self.assertEqual(self.order.status, 'PL') # Order.PLACED by default
        self.order.status = Order.PROCESSING
        self.assertEqual(self.order.status, 'PR')
        self.order.status = Order.COMPLETE
        self.assertEqual(self.order.status, 'CO')
        self.order.status =  Order.DELIVERED
        self.assertEqual(self.order.status, 'DE')
        self.order.status =  Order.CANCELED
        self.assertEqual(self.order.status, 'CA')


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
        self.customer = User.objects.create(
            username='JohnDoe',
            email='john.doe@test.mail',
            password='testPass123'
        )
        # self.item = Product.objects.create(
        #     title='Lighter',
        #     decription='Just a basic lighter'
        # )
        self.order = Order.objects.create(
            customer=self.customer
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

        self.shipment.shipping_method = Shipment.JEFF_BEZOS
        self.assertEqual(self.shipment.shipping_method, 'JB')

    def test_shipment_order_add(self):
        self.shipment.order = self.order
        self.assertTrue(self.shipment.order)
        self.assertEqual(self.shipment.order.customer.username, 'JohnDoe')