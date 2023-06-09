# Generated by Django 4.1.4 on 2023-04-09 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partner",
            name="email",
            field=models.EmailField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="partner",
            name="state",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="partner",
            name="street",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="partner",
            name="telephone",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="partner",
            name="town",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
