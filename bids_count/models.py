from datetime import datetime

from django.db import models


# Create your models here.
class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    # object_id = models.TextField(blank=True, null=True)
    # object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    # change_message = models.TextField()
    # content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    # user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    @staticmethod
    def created_in_current_month():
        #   Надо отсеять события добавления пользователей

        return DjangoAdminLog.objects\
            .filter(action_time__month=datetime.now().month)\
            .filter(action_flag=1)

    class Meta:
        managed = False
        db_table = 'django_admin_log'

