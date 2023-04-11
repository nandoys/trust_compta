# Generated by Django 4.1.4 on 2023-04-11 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0007_customerbill_amount_supplierbill_amount_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customerbill",
            name="amount_foreign_currency",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="customerbill",
            name="rate",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="customerbillpayment",
            name="amount_foreign_currency",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="customerbillpayment",
            name="rate",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="supplierbill",
            name="amount_foreign_currency",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="supplierbill",
            name="rate",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="supplierbillpayment",
            name="amount_foreign_currency",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="supplierbillpayment",
            name="rate",
            field=models.IntegerField(default=1),
        ),
    ]