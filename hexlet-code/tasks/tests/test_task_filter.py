import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from statuses.models import Status
from labels.models import Label


@pytest.mark.django_db
class TestTaskFiltering:

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

        self.author = User.objects.create_user(username='author',
                                               first_name='Имя',
                                               last_name='Фамилия',
                                               password='123')
        self.executor = User.objects.create_user(username='executor',
                                                 first_name='Эк',
                                                 last_name='Сполнитель',
                                                 password='123')
        self.other_user = User.objects.create_user(username='other',
                                                   password='123')

        self.status = Status.objects.create(name='In progress')
        self.label = Label.objects.create(name='Bug')

        self.task = Task.objects.create(
            name='Test task',
            description='Some description',
            status=self.status,
            author=self.author,
            executor=self.executor
        )
        self.task.labels.add(self.label)

        self.client.force_login(self.author)

    def test_filter_by_status(self):
        response = self.client.get(reverse('task_list'),
                                   {'status': self.status.pk})
        assert response.status_code == 200
        assert self.task.name in response.content.decode()

    def test_filter_by_executor(self):
        response = self.client.get(reverse('task_list'),
                                   {'executor': self.executor.pk})
        assert response.status_code == 200
        assert self.task.name in response.content.decode()

    def test_filter_by_label(self):
        response = self.client.get(reverse('task_list'),
                                   {'labels': self.label.pk})
        assert response.status_code == 200
        assert self.task.name in response.content.decode()

    def test_filter_by_self_tasks(self):
        response = self.client.get(reverse('task_list'), {'self_tasks': 'on'})
        assert response.status_code == 200
        assert self.task.name in response.content.decode()

    def test_filter_hides_non_self_tasks(self):
        self.client.logout()
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('task_list'), {'self_tasks': 'on'})
        assert self.task.name not in response.content.decode()
