from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from . import views


class HomePageTests(SimpleTestCase):

    def setUp(self):
        self.home = self.client.get(reverse('pages:home'))
        self.categories = self.client.get(reverse('pages:categories'))
        self.about = self.client.get(reverse('pages:about'))
        self.contact = self.client.get(reverse('pages:contact'))
        self.privacy = self.client.get(reverse('pages:privacy'))


    def test_pages_url_names(self):
        self.assertEqual(self.home.status_code, 200)
        self.assertEqual(self.categories.status_code, 200)
        self.assertEqual(self.about.status_code, 200)
        self.assertEqual(self.contact.status_code, 200)
        self.assertEqual(self.privacy.status_code, 200)

    def test_pages_templates(self):
        self.assertTemplateUsed(self.home, 'home.html')
        self.assertTemplateUsed(self.categories, 'categories.html')
        self.assertTemplateUsed(self.about, 'about.html')
        self.assertTemplateUsed(self.contact, 'contact.html')
        self.assertTemplateUsed(self.privacy, 'privacy.html')

    def test_pages_contain_correct_html(self):
        # For now, just a basic content check
        self.assertContains(self.home, 'Home!')
        self.assertContains(self.categories, 'Categories')
        self.assertContains(self.about, 'About')
        self.assertContains(self.contact, 'Contact')
        self.assertContains(self.privacy, 'Privacy Policy')


    def test_pages_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.home, 'This text is not on the page :)')
        self.assertNotContains(self.categories, 'Text that is not in categories! :_)')
        self.assertNotContains(self.about, 'Somethin not in the About page.')
        self.assertNotContains(self.contact, 'A paragraph that is actually in about page.')
        self.assertNotContains(self.privacy, 'We are the Google Singularity! We are here to store every moment of your life...')

    def test_pages_url_view_resolves(self):
        home_view = resolve('/')
        self.assertEqual(home_view.func.__name__, views.home.__name__)

        categories_view = resolve('/categories/')
        self.assertEqual(categories_view.func.__name__, views.categories.__name__)

        about_view = resolve('/about/')
        self.assertEqual(about_view.func.__name__, views.about.__name__)

        contact_view = resolve('/contact/')
        self.assertEqual(contact_view.func.__name__, views.contact.__name__)

        privacy_view = resolve('/privacy/')
        self.assertEqual(privacy_view.func.__name__, views.privacy.__name__)


# TODO, refactor the tests with a better design for each one
# try to automate the, keep it DRY, at least for the basic tests
class CategoriesPageTests(SimpleTestCase):

    def setUp(self):
        self.page = self.client.get('categories/')
