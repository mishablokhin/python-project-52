import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.apps.labels.models import Label
from django.core.management import call_command


@pytest.mark.django_db
class TestLabelsCRUD:

    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        call_command('loaddata', 'labels_fixture.json')

        self.client = client
        self.user = User.objects.create_user(username='testuser',
                                             password='123')
        self.client.force_login(self.user)

    def test_create_label(self):
        response = self.client.post(reverse('label_create'),
                                    {'name': 'Новая метка'})
        assert response.status_code == 302
        assert Label.objects.filter(name='Новая метка').exists()

    def test_update_label(self):
        label = Label.objects.get(pk=1)
        response = self.client.post(reverse('label_update', args=[label.pk]),
                                    {'name': 'Обновлённая метка'})
        assert response.status_code == 302
        label.refresh_from_db()
        assert label.name == 'Обновлённая метка'

    def test_delete_label(self):
        label = Label.objects.get(pk=2)
        response = self.client.post(reverse('label_delete', args=[label.pk]))
        assert response.status_code == 302
        assert not Label.objects.filter(pk=label.pk).exists()
