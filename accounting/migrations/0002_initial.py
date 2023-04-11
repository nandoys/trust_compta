# Generated by Django 4.1.4 on 2023-04-09 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("treasury", "0001_initial"),
        ("accounting", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="currency",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="treasury.currency",
            ),
        ),
        migrations.AddField(
            model_name="monitoring",
            name="accounting",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounting.additional"
            ),
        ),
        migrations.AddField(
            model_name="monitoring",
            name="year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounting.fiscalyear"
            ),
        ),
        migrations.AddField(
            model_name="budget",
            name="accounting",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounting.additional",
            ),
        ),
        migrations.AddField(
            model_name="adjunct",
            name="account_additional",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounting.additional"
            ),
        ),
        migrations.AddField(
            model_name="additional",
            name="account_main",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounting.main"
            ),
        ),
        migrations.AddConstraint(
            model_name="plan",
            constraint=models.UniqueConstraint(
                fields=("account_number",), name="unique_account_number"
            ),
        ),
        migrations.AddConstraint(
            model_name="plan",
            constraint=models.UniqueConstraint(
                fields=("account_name",), name="unique_account_name"
            ),
        ),
        migrations.AddConstraint(
            model_name="plan",
            constraint=models.UniqueConstraint(
                fields=("account_number", "account_name"),
                name="unique_account_number_name",
            ),
        ),
        migrations.AddConstraint(
            model_name="monitoring",
            constraint=models.UniqueConstraint(
                fields=("accounting", "year"), name="unique_alert"
            ),
        ),
        migrations.AddConstraint(
            model_name="budget",
            constraint=models.UniqueConstraint(
                fields=("accounting", "plan_at"), name="unique_budget"
            ),
        ),
    ]