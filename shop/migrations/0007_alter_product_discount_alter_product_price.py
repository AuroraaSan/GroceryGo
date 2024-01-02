# Generated by Django 4.1 on 2024-01-02 13:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0006_alter_product_discount_alter_product_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="discount",
            field=models.FloatField(
                default=0.0,
                validators=[
                    django.core.validators.MaxValueValidator(100.0),
                    django.core.validators.MinValueValidator(0.0),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.FloatField(),
        ),
    ]
