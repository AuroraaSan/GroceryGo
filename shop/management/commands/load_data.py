import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from ...models import Product, Category, Company
import os
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()


def generate_manufacturing_expiry_dates():
    # Generate a manufacturing date (within the last year)
    manufacturing_date = fake.date_time_between(start_date="-1y", end_date="now")

    # Generate an expiry date (manufacturing date + random duration)
    expiry_duration = random.randint(30, 365)  # Random duration between 30 and 365 days
    expiry_date = manufacturing_date + timedelta(days=expiry_duration)

    return manufacturing_date, expiry_date


class Command(BaseCommand):
    help = "Load data from CSV into Django models"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(os.path.dirname(__file__), "products.csv")

        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Create a dictionary to store parent categories
            parent_categories = {}

            # Iterate over the CSV rows to create parent categories
            for row in reader:
                category_1 = row.get("Category_1", "Generic")

                if category_1 and category_1 not in parent_categories:
                    # Create or get the parent category instance
                    parent_category, created = Category.objects.get_or_create(
                        category_name=category_1, defaults={"parent_cat": None}
                    )
                    parent_categories[category_1] = parent_category
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully created parent category: {category_1}"
                        )
                    )

            # Reset the CSV reader to the beginning of the file
            file.seek(0)
            next(reader)  # Skip the header row

            # Iterate over the CSV rows to create child categories and products
            for row in reader:
                category_1 = row.get("Category_1", "Generic")
                category_2 = row.get("Category_2", "")
                product_name = row.get("Name", "")
                description = row.get("Description", "")
                price = float(row.get("Price", 0.0))
                stock = int(row.get("Stock", 10))
                discount = float(row.get("Discount", 0.0))
                manufacture_date, expiry_date = generate_manufacturing_expiry_dates()
                total_users_purchased = int(row.get("total_users_purchased", 0))
                users_purchased_last_24_hours = int(row.get("users_purchased_last_24_hours", 0))
                p_image = row.get("NewImage", "")
                company_name = row.get("Brand", "")
                if category_2 == "" or company_name == "" or category_1 == "":
                    continue
                # Get the parent category instance
                parent_category = parent_categories.get(category_1)
                # Create or get the child category instance
                if category_2 != "":
                    child_category, created = Category.objects.get_or_create(
                        category_name=category_2,
                        defaults={"parent_cat": parent_category},
                    )
                # Create or get Company instance
                company, created = Company.objects.get_or_create(
                    company_name=company_name,
                    defaults={
                        "description": "",
                        "contact_num": "",
                        "email": "",
                        "nationality": "EGY",
                    },
                )
                if category_2 == "":
                    company.speciality.add(parent_category)
                else:
                    company.speciality.add(parent_category, child_category)
                company.save()

                # Create Product instance
                product = Product.objects.create(
                    product_name=product_name,
                    description=description,
                    price=price,
                    stock=stock,
                    discount=discount,
                    manfacture_date=manufacture_date,
                    expiry_date=expiry_date,
                    total_users_purchased=total_users_purchased,
                    users_purchased_last_24_hours=users_purchased_last_24_hours,
                    p_image=p_image,
                    company_id=company.company_id,
                    cat_id=child_category.cat_id,
                )

                # Update the product slug
                product.slug = slugify(product_name)
                product.save()

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created product: {product_name}")
                )
