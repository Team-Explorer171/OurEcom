from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import ProductModel, SubCategoryModel
from .forms import SubCategoryForm, ProductForm


# Create your views here.
def store(request):
    products = ProductModel.objects.filter(status=True)
    sub_categories = SubCategoryModel.objects.filter(status=True)

    content = {
        'products': products,
        'sub_categories': sub_categories,
    }
    return render(request, 'App_store/store.html', context=content)

