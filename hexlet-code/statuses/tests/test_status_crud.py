import pytest
from django.urls import reverse
from statuses.models import Status
from django.contrib.auth.models import User
from django.core.management import call_command


@pytest.mark.django_db
class TestStatusCRUD:

    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        call_command('loaddata', 'statuses_fixture.json')
        self.client = client
        self.user = User.objects.create_user(username='testuser', password='123')
        self.client.force_login(self.user)

    def test_create_status(self):
        response = self.client.post(reverse('status_create'), {'name': 'Тестовый статус'})
        assert response.status_code == 302
        assert Status.objects.filter(name='Тестовый статус').exists()

    def test_update_status(self):
        status = Status.objects.get(pk=1)
        response = self.client.post(reverse('status_update', args=[status.pk]), {'name': 'Обновлённый статус'})
        assert response.status_code == 302
        status.refresh_from_db()
        assert status.name == 'Обновлённый статус'

    def test_delete_status(self):
        status = Status.objects.get(pk=2)
        response = self.client.post(reverse('status_delete', args=[status.pk]))
        assert response.status_code == 302
        assert not Status.objects.filter(pk=status.pk).exists()