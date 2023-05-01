# Generated by Django 4.1.4 on 2023-04-16 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("treasury", "0013_accountingentry_ref_bill_line"),
        ("accounting", "0008_alter_tax_type_journal"),
    ]

    operations = [
        migrations.AddField(
            model_name="tax",
            name="currency",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="treasury.currency",
            ),
        ),
    ]