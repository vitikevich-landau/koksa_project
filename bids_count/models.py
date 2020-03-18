from datetime import datetime

from django.db import models


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(DjangoContentType, models.CASCADE, blank=True, null=True)

    # user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    @staticmethod
    def created_in_current_month():
        #   Оставляем только события добавления записи в нашу модель
        #   content_type=7 - создание новости
        #   action_flag=1 - создание
        return DjangoAdminLog.objects \
            .filter(content_type=7) \
            .filter(action_time__month=datetime.now().month) \
            .filter(action_flag=1)

    class Meta:
        managed = False
        db_table = 'django_admin_log'
