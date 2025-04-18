from django.db import models
from django.contrib.auth.models import User
from task_manager.apps.statuses.models import Status
from task_manager.apps.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    description = models.TextField(blank=True, verbose_name='Описание')
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               verbose_name='Статус')
    author = models.ForeignKey(User,
                               on_delete=models.PROTECT,
                               related_name='created_tasks',
                               verbose_name='Автор')
    executor = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 related_name='executed_tasks',
                                 null=True,
                                 blank=True, verbose_name='Исполнитель')
    labels = models.ManyToManyField(Label, blank=True,
                                    related_name='tasks',
                                    verbose_name='Метки')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')

    def __str__(self):
        return self.name
