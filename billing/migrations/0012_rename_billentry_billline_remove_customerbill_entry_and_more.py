# Generated by Django 4.1.4 on 2023-04-13 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0002_initial"),
        ("billing", "0011_alter_customerbill_amount_alter_customerbill_entry"),
    ]

    operations = [
        migrations.RenameModel(old_name="BillEntry", new_name="BillLine",),
        migrations.RemoveField(model_name="customerbill", name="entry",),
        migrations.RemoveField(model_name="supplierbill", name="entry",),
        migrations.AddField(
            model_name="customerbill",
            name="bill_lines",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="customer_bill_lines",
                to="billing.billline",
            ),
        ),
        migrations.AddField(
            model_name="supplierbill",
            name="bill_lines",
            field=models.ManyToManyField(
                blank=True, related_name="supplier_bill_lines", to="billing.billline"
            ),
        ),
    ]
