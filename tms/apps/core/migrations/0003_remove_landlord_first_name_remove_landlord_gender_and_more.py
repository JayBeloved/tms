# Generated by Django 4.1.3 on 2022-11-24 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_rentals_agreement_duration"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="landlord",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="landlord",
            name="gender",
        ),
        migrations.RemoveField(
            model_name="landlord",
            name="last_name",
        ),
        migrations.AddField(
            model_name="landlord",
            name="landlord_name",
            field=models.CharField(max_length=100, null=True),
        ),
    ]