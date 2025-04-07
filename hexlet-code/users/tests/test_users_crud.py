import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_create(client):
    url = reverse('register')
    data = {
        'first_name': 'Ivan',
        'last_name': 'Petrov',
        'username': 'ivan123',
        'password1': 'testpass123',
        'password2': 'testpass123',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.filter(username='ivan123').exists()


@pytest.mark.django_db
def test_user_update(client, django_user_model):
    user = django_user_model.objects.create_user(username='ivan', password='1234')
    client.login(username='ivan', password='1234')

    url = reverse('user_update', args=[user.pk])
    data = {
        'first_name': 'Ivan',
        'last_name': 'Updated',
        'username': 'ivan',
        'password1': '',
        'password2': '',
    }
    response = client.post(url, data)
    user.refresh_from_db()
    assert response.status_code == 302
    assert user.last_name == 'Updated'


@pytest.mark.django_db
def test_user_delete(client, django_user_model):
    user = django_user_model.objects.create_user(username='ivan', password='1234')
    client.login(username='ivan', password='1234')

    url = reverse('user_delete', args=[user.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert not User.objects.filter(pk=user.pk).exists()