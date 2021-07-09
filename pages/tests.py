from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from . import views


class HomePageTests(SimpleTestCase):


    def setUp(self):
        self.homepage = self.client.get(reverse('pages:home'))


    def test_homepage_url_name(self):
        # Actually saved me time from the first run, had a typo - nome :D
        self.assertEqual(self.homepage.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.homepage, 'home.html')

    def test_homepage_contains_correct_html(self):
        # For now, just a basic content check
        self.assertContains(self.homepage, 'Home!')

    def test_homepage_does_not_contains_incorrect_html(self):
        self.assertNotContains(self.homepage, 'This text is not on the page :)')

    def test_homepage_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, views.home.__name__)
