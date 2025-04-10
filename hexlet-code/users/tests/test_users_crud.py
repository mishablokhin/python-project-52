import pytest
from django.core.management import call_command
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestUserCRUD:

    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        call_command('loaddata', 'users')
        self.client = client
        self.user = User.objects.get(username='ivan')

    def test_user_create(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Ivan',
            'last_name': 'Petrov',
            'username': 'ivan123',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        assert response.status_code == 302
        assert User.objects.filter(username='ivan123').exists()

    def test_user_update(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('user_update', args=[self.user.pk]), {
            'first_name': 'Ivan',
            'last_name': 'Updated',
            'username': 'ivan',
            'password1': '',
            'password2': '',
        })
        self.user.refresh_from_db()
        assert response.status_code == 302
        assert self.user.last_name == 'Updated'

    def test_user_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('user_delete', args=[self.user.pk]))
        assert response.status_code == 302
        assert not User.objects.filter(pk=self.user.pk).exists()
