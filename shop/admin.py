from django.contrib import admin
from .models import Product, Category, Company

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "p_id",
        "product_name",
        "price",
        "stock",
        "discount",
        "cat_id",
        "company_id",
        "total_users_purchased",
        "users_purchased_last_24_hours",
    ]
    raw_id_fields = ["cat", "company"]
    list_filter = ["price", "total_users_purchased", "users_purchased_last_24_hours", "cat_id", "company_id"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["cat_id", "category_name", "parent_cat"]
    search_fields = ["category_name"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "company_id",
        "company_name",
        "contact_num",
        "email",
        "nationality",
        "get_specialities_display",
    ]
    list_filter = ["nationality", "speciality"]
    search_fields = ["company_name", "nationality"]

    def get_specialities_display(self, obj):
        return ", ".join(
            [speciality.category_name for speciality in obj.speciality.all()]
        )

    get_specialities_display.short_description = "Specialities"

    def save_model(self, request, obj, form, change):
        # Save the Company instance
        obj.save()

        # Get the list of category names from the form data
        categories_names = form.cleaned_data.get("speciality", [])

        # Add specialities to the Company instance without overwriting existing ones
        for category_name in categories_names:
            category_instance, created = Category.objects.get_or_create(
                category_name=category_name
            )
            obj.speciality.add(category_instance)

        # Save the Company instance after adding specialities
        obj.save()
