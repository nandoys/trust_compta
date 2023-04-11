import uuid
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Role(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name
