# Generated by Django 4.1.4 on 2023-04-15 10:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0004_remove_tax_calculation_tax_is_fixed_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TypeTax",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={"db_table": "accounting_type_tax",},
        ),
        migrations.AlterModelOptions(
            name="tax", options={"verbose_name_plural": "Taxes"},
        ),
        migrations.AddField(
            model_name="tax",
            name="type_tax",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="accounting.typetax",
            ),
        ),
    ]
