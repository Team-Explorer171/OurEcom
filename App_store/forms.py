from django import forms
from App_store.models import SubCategoryModel, ProductModel


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategoryModel
        exclude = ['status', 'created', ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        exclude = ['status', 'created', ]

