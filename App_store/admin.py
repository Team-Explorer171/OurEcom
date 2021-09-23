from django.contrib import admin
from .models import SubCategoryModel, ProductModel

# Register your models here.

admin.site.register(SubCategoryModel)
admin.site.register(ProductModel)
