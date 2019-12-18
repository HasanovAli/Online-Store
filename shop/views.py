from django.shortcuts import render, get_object_or_404

from .models import Product, Category
from bucket.forms import BucketAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    bucket_product_form = BucketAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'bucket_product_form': bucket_product_form})
