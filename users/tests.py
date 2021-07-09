from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='test',
            password='testpass123',
            email='test@test.com'
        )
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        su = User.objects.create_superuser(
            username='su_test',
            password='suTestPass@5',
            email='su@admin.com'
        )
        self.assertEqual(su.username, 'su_test')
        self.assertEqual(su.email, 'su@admin.com')
        self.assertTrue(su.check_password('suTestPass@5'))
        self.assertTrue(su.is_active)
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)
