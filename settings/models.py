import uuid
from django.db import models
from treebeard.mp_tree import MP_Node


class Journal(MP_Node):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)
    account = models.ForeignKey('accounting.Plan', on_delete=models.CASCADE)
    type_journal = models.ForeignKey('JournalType', on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_module_name'),
        ]


class JournalType(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    label = models.CharField(max_length=255, unique=True)
