"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import IndexView
from django.contrib import admin
from task_manager.views import CustomLoginView, CustomLogoutView
from django.urls import include

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # Django admin
    path('admin/', admin.site.urls),

    # Аутентификация
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('users/', include('task_manager.apps.users.urls')),

    path('statuses/', include('task_manager.apps.statuses.urls')),

    path('tasks/', include('task_manager.apps.tasks.urls')),

    path('labels/', include('task_manager.apps.labels.urls')),
]
