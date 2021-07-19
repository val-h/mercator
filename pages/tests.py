from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from . import views


# The basic tests will not be running DRY, for now this works
# and doesn't complicate the tests
class BasicPageTests(SimpleTestCase):

    def setUp(self):
        self.home = self.client.get(reverse('pages:home'))

    def test_page_url_name(self):
        self.assertEqual(self.home.status_code, 200)

    def test_pages_templates(self):
        self.assertTemplateUsed(self.home, 'home.html')

    def test_pages_contain_correct_html(self):
        # For now, just a basic content check
        self.assertContains(self.home, 'Home!')

    def test_pages_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.home, 'This text is not on the page :)')

    def test_pages_url_view_resolves(self):
        home_view = resolve('/')
        self.assertEqual(home_view.func.__name__, views.home.__name__)


class CategoriesPageTests(SimpleTestCase):

    def setUp(self):
        self.page = self.client.get(reverse('pages:categories'))

    def test_categories_url_name(self):
        self.assertEqual(self.page.status_code, 200)

    def test_categories_template(self):
        self.assertTemplateUsed(self.page, 'categories.html')
    
    def test_categories_url_view_resolve(self):
        page_view = resolve('/categories/')
        self.assertEqual(page_view.func.__name__, views.categories.__name__)


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        self.page = self.client.get(reverse('pages:about'))

    def test_about_url_name(self):
        self.assertEqual(self.page.status_code, 200)

    def test_about_template(self):
        self.assertTemplateUsed(self.page, 'about.html')

    def test_about_url_view_resolve(self):
        page_view = resolve('/about/')
        self.assertEqual(page_view.func.__name__, views.about.__name__)


class ContactPageTests(SimpleTestCase):
    def setUp(self):
        self.page = self.client.get(reverse('pages:contact'))

    def test_contact_url_name(self):
        self.assertEqual(self.page.status_code, 200)

    def test_contact_template_used(self):
        self.assertTemplateUsed(self.page, 'contact.html')

    def test_contact_url_view_resolve(self):
        page_view = resolve('/contact/')
        self.assertEqual(page_view.func.__name__, views.contact.__name__)


class PrivacyPageTests(SimpleTestCase):
    def setUp(self):
        self.page = self.client.get(reverse('pages:privacy'))

    def test_contact_url_name(self):
        self.assertEqual(self.page.status_code, 200)

    def test_privacy_template_used(self):
        self.assertTemplateUsed(self.page, 'privacy.html')

    def test_privacy_url_view_resolve(self):
        page_view = resolve('/privacy/')
        self.assertEqual(page_view.func.__name__, views.privacy.__name__)


class CartPageTests(SimpleTestCase):
    def setUp(self):
        self.page = self.client.get(reverse('pages:cart'))

    def test_cart_url_name(self):
        self.assertEqual(self.page.status_code, 200)

    def test_cart_template_used(self):
        self.assertTemplateUsed(self.page, 'cart.html')

    def test_cart_url_view_resolve(self):
        page_view = resolve('/cart/')
        self.assertEqual(page_view.func.__name__, views.cart.__name__)


class AccountPageTests(TestCase):
    def setUp(self):
        User = get_user_model()
        test_user = User.objects.create_user(
            email='test@mail.com',
            username='test',
            password='testPass123',
        )
        client = Client()
        client.login(username='test', password='testPass123')
        # Request with authenticated client
        self.auth_page = client.get(reverse('pages:account'))
        # Request with anonymous user
        self.anon_page = self.client.get(reverse('pages:account'))

    def test_account_url_name(self):
        self.assertEqual(self.auth_page.status_code, 200)
        self.assertEqual(self.anon_page.status_code, 302 or 404)

    def test_account_template_used(self):
        self.assertTemplateUsed(self.auth_page, 'account.html')

    def test_account_url_view_resolve(self):
        page_view = resolve('/account/')
        self.assertEqual(page_view.func.__name__, views.account.__name__)


class SearchPageTests(SimpleTestCase):
    def setUp(self):
        self.page = self.client.get(reverse('pages:search', kwargs={'pattern': 'keyword7'}))

    def test_search_url_name(self):
        self.assertEqual(self.page.status_code, 200)

    def test_search_template_used(self):
        self.assertTemplateUsed(self.page, 'search.html')

    def test_search_contains_html(self):
        self.assertContains(self.page, 'keyword7')

    def test_search_does_not_contain_html(self):
        self.assertNotContains(self.page, 'keyword531')
    
    def test_search_url_view_resolve(self):
        page_view = resolve('/search/keyword')
        self.assertEqual(page_view.func.__name__, views.search.__name__)
