from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.
class Category(models.Model):
    cat_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    parent_cat = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.category_name
    
class Company(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    contact_num = models.CharField(max_length=15, null=True)
    email = models.EmailField(blank=True, null=True)
    # nationality to be choices instead of charfield
    nationality = models.CharField(max_length=3) 
    speciality = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return {'Name': self.company_name, 'Description': self.description, 'Speciality': self.speciality}

    
class Product(models.Model):
    p_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    discount = models.FloatField(default=0.0, validators=[
        MaxValueValidator(100.0),
        MinValueValidator(0.0)
    ])
    manfacture_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=False, blank=False)
    purchased_gen = models.IntegerField(default=0)
    purchased_24 = models.IntegerField(default=0)
    company_id = models.ForeignKey(Company, on_delete=models.SET_DEFAULT, null=True, default=1)
    cat_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)