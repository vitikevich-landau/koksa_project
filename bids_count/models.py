from datetime import datetime

from django.db import models


# Create your models here.
class DjangoAdminLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def published_in_the_current_month(self):
        return self.objects.filter(created__month=datetime.now().month)

    class Meta:
        managed = False
        db_table = 'django_admin_log'
