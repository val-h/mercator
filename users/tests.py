from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from .forms import CustomUserCreateForm
from . import views
from .models import Preference
from shop.models import Category


User = get_user_model()


class CustomUserTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username='test',
            password='testpass123',
            email='test@test.com',
            total_items_bought=7,
            total_reviews=2,
        )
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.total_items_bought, 7)
        self.assertEqual(user.total_reviews, 2)
        self.assertEqual(user.account_type, 'C')  # Default

    def test_create_superuser(self):
        User = get_user_model()
        su = User.objects.create_superuser(
            username='su_test',
            password='suTestPass@5',
            email='su@admin.com',
            total_items_bought=1,
            total_reviews=1,
            # Default - Customer from [Customer, Merchant], model for ref
            account_type='M'
        )
        self.assertEqual(su.username, 'su_test')
        self.assertEqual(su.email, 'su@admin.com')
        self.assertTrue(su.check_password('suTestPass@5'))
        self.assertTrue(su.is_active)
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)
        self.assertEqual(su.total_items_bought, 1)
        self.assertEqual(su.total_reviews, 1)
        self.assertEqual(su.account_type, 'M')


class RegisterPageTest(TestCase):

    def setUp(self):
        self.register = self.client.get(reverse('users:register'))

    def test_register_template(self):
        self.assertEqual(self.register.status_code, 200)
        self.assertTemplateUsed(self.register, 'registration/register.html')
        self.assertContains(self.register, 'Register')
        self.assertNotContains(self.register, 'Logout')

    def test_register_form(self):
        form = self.register.context.get('form')
        self.assertIsInstance(form, CustomUserCreateForm)
        self.assertContains(self.register, 'csrfmiddlewaretoken')

    def test_register_view(self):
        view = resolve('/auth/register/')
        self.assertEqual(view.func.__name__, views.register.__name__)


class PreferenceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer',
            password='testpass123',
            email='customer@example.com'
        )
        self.category = Category.objects.create(name='Example')

    def test_user_preference_created(self):
        self.assertTrue(self.user.preferences.first())

    def test_user_preference_category(self):
        self.assertEqual(self.user.preferences.first().category, self.category)

    def test_user_preference_update_method(self):
        preference = self.user.preferences.first()
        self.assertFalse(preference.last_search)
        self.assertEqual(preference.search_modifier, 0)
        preference.update()
        self.assertTrue(preference.last_search)
        self.assertEqual(preference.search_modifier, 1)
