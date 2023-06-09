# Generated by Django 4.1.4 on 2023-04-11 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0006_customerbillpayment_reference_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customerbill",
            name="amount",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="supplierbill",
            name="amount",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="customerbill",
            name="entry",
            field=models.ManyToManyField(
                related_name="customer_bill_entry", to="billing.billentry"
            ),
        ),
        migrations.AlterField(
            model_name="supplierbill",
            name="entry",
            field=models.ManyToManyField(
                related_name="supplier_bill_entry", to="billing.billentry"
            ),
        ),
    ]
