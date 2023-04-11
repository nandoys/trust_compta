# Generated by Django 4.1.4 on 2023-04-09 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0003_alter_partner_email_alter_partner_state_and_more"),
        ("treasury", "0002_statement_rate"),
    ]

    operations = [
        migrations.RemoveField(model_name="accountingentry", name="slip",),
        migrations.RemoveField(model_name="accountingentry", name="slip_number",),
        migrations.RemoveField(model_name="accountingentry", name="tier",),
        migrations.AddField(
            model_name="accountingentry",
            name="partner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="billing.partner",
            ),
        ),
        migrations.AddField(
            model_name="accountingentry",
            name="ref_billing_customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="billing.customerbill",
            ),
        ),
        migrations.AddField(
            model_name="accountingentry",
            name="ref_billing_supplier",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="billing.supplierbill",
            ),
        ),
        migrations.AddField(
            model_name="accountingentry",
            name="ref_statement",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="treasury.statement",
            ),
        ),
    ]
