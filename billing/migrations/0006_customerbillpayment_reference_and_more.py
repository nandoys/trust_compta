# Generated by Django 4.1.4 on 2023-04-11 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0005_supplierbillpayment_customerbillpayment"),
    ]

    operations = [
        migrations.AddField(
            model_name="customerbillpayment",
            name="reference",
            field=models.CharField(default=str, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="supplierbillpayment",
            name="reference",
            field=models.CharField(default=str, max_length=255),
            preserve_default=False,
        ),
    ]
