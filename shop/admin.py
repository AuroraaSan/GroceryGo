from django.contrib import admin
from .models import Product, Category, Company
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['p_id', 'product_name', 'price', 'stock', 'discount', 'cat_id', 'company_id']
    raw_id_fields = ['cat', 'company']
    list_filter = ['price', 'purchased_gen', 'purchased_24', 'cat_id', 'company_id']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cat_id', 'category_name', 'parent_cat']
    search_fields = ['category_name']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'company_name', 'contact_num', 'email', 'nationality', 'get_specialities_display']
    list_filter = ['nationality', 'speciality']
    search_fields = ['company_name', 'nationality']

    def get_specialities_display(self, obj):
        return ", ".join([speciality.category_name for speciality in obj.speciality.all()])
    get_specialities_display.short_description = 'Specialities'