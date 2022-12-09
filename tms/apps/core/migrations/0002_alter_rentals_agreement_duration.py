# Generated by Django 4.1.3 on 2022-11-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rentals",
            name="agreement_duration",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "6 Months"),
                    (2, "1 Year"),
                    (3, "18 Months"),
                    (4, "2 Years"),
                    (5, "3 Years"),
                    (6, "5 Years"),
                ],
                default=2,
                verbose_name="agreement duration",
            ),
        ),
    ]
