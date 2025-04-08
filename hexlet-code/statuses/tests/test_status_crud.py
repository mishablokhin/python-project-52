import pytest
from django.urls import reverse
from statuses.models import Status

@pytest.mark.django_db
class TestStatusCRUD:

    @pytest.fixture(autouse=True)
    def setup(self, client, django_user_model, db, settings):
        self.client = client
        self.user = django_user_model.objects.create_user(username='testuser', password='123')
        self.client.force_login(self.user)

    def test_create_status(self):
        response = self.client.post(reverse('status_create'), {'name': 'Тестовый статус'})
        assert response.status_code == 302
        assert Status.objects.filter(name='Тестовый статус').exists()

    def test_update_status(self):
        status = Status.objects.create(name='Старый статус')
        response = self.client.post(reverse('status_update', args=[status.pk]), {'name': 'Новый статус'})
        assert response.status_code == 302
        status.refresh_from_db()
        assert status.name == 'Новый статус'

    def test_delete_status(self):
        status = Status.objects.create(name='Удаляемый статус')
        response = self.client.post(reverse('status_delete', args=[status.pk]))
        assert response.status_code == 302
        assert not Status.objects.filter(pk=status.pk).exists()