# Generated by Django 4.1 on 2023-12-30 14:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0005_alter_company_nationality"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="discount",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=5,
                validators=[
                    django.core.validators.MaxValueValidator(100.0),
                    django.core.validators.MinValueValidator(0.0),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
