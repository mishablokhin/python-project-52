import pytest
from django.urls import reverse
from task_manager.apps.tasks.models import Task
from django.contrib.auth.models import User
from task_manager.apps.statuses.models import Status
from django.core.management import call_command


@pytest.mark.django_db
class TestTasksCRUD:

    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        call_command('loaddata', 'tasks.json')

        self.client = client
        self.author = User.objects.get(username='author')
        self.other = User.objects.get(username='otheruser')
        self.status = Status.objects.get(pk=1)

    def login(self, user):
        self.client.force_login(user)

    def test_create_task(self):
        self.login(self.author)
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'Test Description',
            'status': self.status.pk,
            'executor': self.other.pk,
        })
        assert response.status_code == 302
        assert Task.objects.filter(name='New Task').exists()

    def test_update_task(self):
        self.login(self.author)
        task = Task.objects.create(
            name='Old Name',
            description='Old Desc',
            status=self.status,
            author=self.author,
            executor=self.other
        )
        response = self.client.post(reverse('task_update', args=[task.pk]), {
            'name': 'Updated Name',
            'description': 'Updated Desc',
            'status': self.status.pk,
            'executor': self.other.pk,
        })
        task.refresh_from_db()
        assert response.status_code == 302
        assert task.name == 'Updated Name'

    def test_delete_task_by_author(self):
        self.login(self.author)
        task = Task.objects.create(
            name='Delete Me',
            description='...',
            status=self.status,
            author=self.author,
            executor=self.other
        )
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        assert response.status_code == 302
        assert not Task.objects.filter(pk=task.pk).exists()

    def test_delete_task_by_non_author(self):
        self.login(self.other)
        task = Task.objects.create(
            name='Secure Task',
            description='...',
            status=self.status,
            author=self.author,
            executor=self.other
        )
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        assert response.status_code == 302
        assert Task.objects.filter(pk=task.pk).exists()
