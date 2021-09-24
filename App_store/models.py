from django.db import models
from django_mysql.models import ListCharField

# Create your models here.

category_choice = (
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Children', 'Children'),
    ('Special Collection', 'Special Collection'),
)


class SubCategoryModel(models.Model):
    category = models.CharField(choices=category_choice, max_length=20)
    sub_category = models.CharField(max_length=50, unique=True)
    status = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)


class ProductModel(models.Model):
    product_header_image = models.ImageField(upload_to='product_image')
    product_image_1 = models.ImageField(upload_to='product_image')
    product_image_2 = models.ImageField(upload_to='product_image')
    product_image_3 = models.ImageField(upload_to='product_image')
    product_name = models.CharField(max_length=200)
    category = models.CharField(choices=category_choice, max_length=20)
    product_sub_category = models.ForeignKey('SubCategoryModel', on_delete=models.CASCADE, related_name='product_sub_category')
    quantity = models.PositiveIntegerField()
    available_colors = ListCharField(base_field=models.CharField(max_length=50), size=10, max_length=(10 * 51),
                                     blank=True, null=True)
    available_sizes = ListCharField(base_field=models.CharField(max_length=50), size=8, max_length=(8 * 51), blank=True,
                                    null=True)
    initial_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    product_description = models.TextField()
    status = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)

