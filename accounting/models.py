from django.db import models
from treebeard.mp_tree import MP_Node, MP_NodeManager
import uuid


class Main(models.Model):
    types = [('encaissement', 'encaissement'), ('decaissement', 'decaissement')]
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    account_number = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255, unique=True)
    account_type = models.CharField(max_length=255, choices=types)
    account_classification = models.CharField(max_length=255)
    account_description = models.TextField(max_length=500, null=True, blank=True)
    can_credit = models.BooleanField(default=False)
    can_debit = models.BooleanField(default=False)

    def __str__(self):
        return self.account_name


class Additional(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    account_number = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255, unique=True)
    account_description = models.TextField(max_length=500, null=True, blank=True)
    account_main = models.ForeignKey(Main, on_delete=models.CASCADE)

    def __str__(self):
        return self.account_name


class Adjunct(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    account_additional = models.ForeignKey(Additional, on_delete=models.CASCADE)
    adjunct_account_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.adjunct_account_name


class PlanManager(MP_NodeManager):

    # method to render tree hierarchy
    def get_tree(self, *args, **kwargs) -> list:
        result = list()
        root_qs = self.filter(depth=1).all()
        children_qs = self.filter(depth=2).all()
        custom_qs = self.filter(depth=3).all()

        root_nodes = root_qs.values_list('id', 'account_namz', 'account_number', 'category', 'path')
        children_nodes = children_qs.values_list('id', 'account_namz', 'account_number', 'path')
        custom_nodes = custom_qs.values_list('id', 'account_namz', 'account_number', 'path')

        for root in root_nodes:
            children = list()
            for child in children_nodes:
                customs = list()
                if str(child[3]).startswith(root[4]):
                    for custom in custom_nodes:
                        if str(custom[3]).startswith(child[3]):
                            customs.append({
                                'id': custom[0],
                                'account_namz': custom[1],
                                'account_numer': custom[2],
                            })
                    children.append({
                        'id': child[0],
                        'account_namz': child[1],
                        'account_numer': child[2],
                        'children': customs
                    })
            result.append({
                'id': root[0],
                'account_namz': root[1],
                'account_numer': root[2],
                'group': root[3],
                'children': children
            })
        return result


class Plan(MP_Node):
    file_type = [('csv', 'csv'), ('excel', 'excel')]
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=500)
    category = models.ForeignKey('PlanCategory', on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True, default=None, blank=True)
    allow_lettering = models.BooleanField(default=False)
    load_from = models.CharField(max_length=10, choices=file_type, null=True, blank=True)
    manager = PlanManager()

    node_order_by = ['account_number']

    def __str__(self):
        return str(self.account_number) + ' ' + str(self.account_name)

    class Meta:
        db_table = 'accounting_plan'
        constraints = [
            models.UniqueConstraint(fields=['account_number'], name='unique_account_number'),

            models.UniqueConstraint(fields=['account_name'], name='unique_account_name'),

            models.UniqueConstraint(fields=['account_number', 'account_name'], name='unique_account_number_name'),
        ]


class PlanCategory(MP_Node):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50)

    node_order_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'accounting_plan_category'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name'),
        ]


class FiscalYear(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    year = models.IntegerField(unique=True)
    rate = models.IntegerField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.year)


class Budget(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    accounting = models.ForeignKey(Additional, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
    plan_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.accounting.account_name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['accounting', 'plan_at'], name='unique_budget'),
        ]


class Monitoring(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    accounting = models.ForeignKey(Additional, on_delete=models.CASCADE)
    warn_at = models.FloatField()
    year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    message = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['accounting', 'year'], name='unique_alert'),
        ]


class Document(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    reference = models.CharField(max_length=255)
    label = models.CharField(max_length=255, null=True, blank=True)
    account = models.ForeignKey(Plan, on_delete=models.CASCADE)
    partner = models.ForeignKey('billing.Partner', on_delete=models.SET_NULL, null=True, blank=True)
    can_edit = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Tax(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    account = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    currency = models.ForeignKey('treasury.Currency', on_delete=models.CASCADE, null=True, blank=True)
    is_fixed = models.BooleanField()
    type_journal = models.ForeignKey('settings.JournalType', on_delete=models.SET_NULL, null=True, related_name='tax_journal_type')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Taxes'

