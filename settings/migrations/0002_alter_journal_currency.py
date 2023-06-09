# Generated by Django 4.1.4 on 2023-04-13 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("treasury", "0010_alter_accountingentry_account_and_more"),
        ("settings", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="journal",
            name="currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="treasury.currency",
            ),
        ),
    ]
