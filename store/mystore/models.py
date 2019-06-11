from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Base(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,related_name="%(app_label)s_%(class)s_created")
    updated_by = models.ForeignKey(User,related_name="%(app_label)s_%(class)s_updated")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

class Box(Base):
    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    def __str__(self):
        return str((self.created_by))



