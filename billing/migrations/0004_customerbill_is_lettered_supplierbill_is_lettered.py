# Generated by Django 4.1.4 on 2023-04-10 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0003_alter_partner_email_alter_partner_state_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customerbill",
            name="is_lettered",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="supplierbill",
            name="is_lettered",
            field=models.BooleanField(default=False),
        ),
    ]
