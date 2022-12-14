# Generated by Django 4.1.3 on 2022-11-22 19:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="landlord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=25)),
                ("last_name", models.CharField(max_length=30)),
                (
                    "gender",
                    models.CharField(
                        choices=[("Male", "Male"), ("Female", "Female")],
                        default="Male",
                        max_length=10,
                    ),
                ),
                ("landlord_email", models.EmailField(max_length=254, null=True)),
                (
                    "mobile_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "state_of_origin",
                    models.CharField(
                        choices=[
                            ("Abia", "Abia"),
                            ("Adamawa", "Adamawa"),
                            ("Akwa-Ibom", "Akwa-Ibom"),
                            ("Anambra", "Anambra"),
                            ("Bauchi", "Bauchi"),
                            ("Bayelsa", "Bayelsa"),
                            ("Borno", "Borno"),
                            ("Cross-River", "Cross-River"),
                            ("Delta", "Delta"),
                            ("Ebonyi", "Ebonyir"),
                            ("Edo", "Edo"),
                            ("Ekiti", "Ekiti"),
                            ("Enugu", "Enugu"),
                            ("Gombe", "Gombe"),
                            ("Imo", "Imo"),
                            ("Jigawa", "Jigawa"),
                            ("Kaduna", "Kaduna"),
                            ("Kano", "Kano"),
                            ("Kastina", "Kastina"),
                            ("Kebbi", "Kebbi"),
                            ("Kogi", "Kogi"),
                            ("Kwara", "Kwara"),
                            ("Lagos", "Lagos"),
                            ("Nassarawa", "Nassarawa"),
                            ("Niger", "Niger"),
                            ("Ogun", "Ogun"),
                            ("Ondo", "Ondo"),
                            ("Osun", "Osun"),
                            ("Oyo", "Oyo"),
                            ("Plateau", "Plateau"),
                            ("Sokoto", "Sokoto"),
                            ("Sokoto", "Sokoto"),
                            ("Taraba", "Taraba"),
                            ("Yobe", "Yobe"),
                            ("Zamfara", "Zamfara"),
                            ("FCT", "FCT"),
                        ],
                        default="FCT",
                        max_length=15,
                    ),
                ),
                (
                    "date_registered",
                    models.DateField(
                        default=datetime.date, null=True, verbose_name="reg_date"
                    ),
                ),
                ("landlord_code", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="managed_properties",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("property_name", models.CharField(max_length=60)),
                ("address", models.CharField(max_length=225)),
                ("city", models.CharField(max_length=100)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("Abia", "Abia"),
                            ("Adamawa", "Adamawa"),
                            ("Akwa-Ibom", "Akwa-Ibom"),
                            ("Anambra", "Anambra"),
                            ("Bauchi", "Bauchi"),
                            ("Bayelsa", "Bayelsa"),
                            ("Borno", "Borno"),
                            ("Cross-River", "Cross-River"),
                            ("Delta", "Delta"),
                            ("Ebonyi", "Ebonyir"),
                            ("Edo", "Edo"),
                            ("Ekiti", "Ekiti"),
                            ("Enugu", "Enugu"),
                            ("Gombe", "Gombe"),
                            ("Imo", "Imo"),
                            ("Jigawa", "Jigawa"),
                            ("Kaduna", "Kaduna"),
                            ("Kano", "Kano"),
                            ("Kastina", "Kastina"),
                            ("Kebbi", "Kebbi"),
                            ("Kogi", "Kogi"),
                            ("Kwara", "Kwara"),
                            ("Lagos", "Lagos"),
                            ("Nassarawa", "Nassarawa"),
                            ("Niger", "Niger"),
                            ("Ogun", "Ogun"),
                            ("Ondo", "Ondo"),
                            ("Osun", "Osun"),
                            ("Oyo", "Oyo"),
                            ("Plateau", "Plateau"),
                            ("Sokoto", "Sokoto"),
                            ("Sokoto", "Sokoto"),
                            ("Taraba", "Taraba"),
                            ("Yobe", "Yobe"),
                            ("Zamfara", "Zamfara"),
                            ("FCT", "FCT"),
                        ],
                        default="FCT",
                        max_length=15,
                    ),
                ),
                ("country", models.CharField(max_length=50)),
                ("description", models.TextField()),
                (
                    "date_registered",
                    models.DateField(
                        default=datetime.date, null=True, verbose_name="reg_date"
                    ),
                ),
                (
                    "property_status",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Occupied"), (0, "Vacant")],
                        default=0,
                        verbose_name="Property Status",
                    ),
                ),
                ("property_code", models.CharField(max_length=30, unique=True)),
                (
                    "landlord",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.landlord"
                    ),
                ),
                (
                    "registered_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="tenant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=25)),
                ("last_name", models.CharField(max_length=30)),
                (
                    "gender",
                    models.CharField(
                        choices=[("Male", "Male"), ("Female", "Female")],
                        default="Male",
                        max_length=10,
                    ),
                ),
                ("tenant_email", models.EmailField(max_length=254, null=True)),
                (
                    "mobile_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "marital_status",
                    models.CharField(
                        choices=[
                            ("Single", "Single"),
                            ("Married", "Married"),
                            ("Divorced", "Divorced"),
                        ],
                        default="Single",
                        max_length=10,
                    ),
                ),
                ("tenant_age", models.CharField(max_length=5)),
                ("nationality", models.CharField(max_length=50)),
                ("spouse_full_name", models.CharField(max_length=70)),
                ("children", models.CharField(max_length=5)),
                ("no_of_dependants", models.CharField(max_length=5)),
                ("occupation", models.CharField(max_length=50)),
                ("industry", models.CharField(max_length=50)),
                ("office_address", models.TextField()),
                (
                    "current_property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.managed_properties",
                        to_field="property_code",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="rentals",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "proposed_use",
                    models.CharField(
                        choices=[
                            ("Residential", "Residential Purpose"),
                            ("Business", "Business Purpose"),
                        ],
                        default="Residential",
                        max_length=20,
                    ),
                ),
                (
                    "date_started",
                    models.DateField(
                        default=datetime.date,
                        null=True,
                        verbose_name="Beginning of Rent",
                    ),
                ),
                (
                    "agreement_duration",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "6 Months"),
                            (2, "1 Year"),
                            (3, "18 Months"),
                            (4, "2 Years"),
                            (5, "3 Years"),
                            (6, "5 Years"),
                        ],
                        default=2,
                        max_length=10,
                    ),
                ),
                ("rental_amount", models.CharField(max_length=30)),
                (
                    "date_ending",
                    models.DateField(null=True, verbose_name="End of Rent"),
                ),
                ("agreement_code", models.CharField(max_length=30, unique=True)),
                (
                    "agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.managed_properties",
                        to_field="property_code",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.tenant"
                    ),
                ),
            ],
        ),
    ]
