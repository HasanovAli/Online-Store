from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .bucket import Bucket
from .forms import BucketAddProductForm


@require_POST
def bucket_add(request, product_id):
    bucket = Bucket(request)
    product = get_object_or_404(Product, id=product_id)
    form = BucketAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        bucket.add(product=product, quantity=cd.get('quantity'), update_quantity=cd.get('update'))
    return redirect('bucket:detail')


def bucket_remove(request, product_id):
    bucket = Bucket(request)
    product = get_object_or_404(Product, id=product_id)
    bucket.remove(product)
    return redirect('bucket:detail')


def bucket_detail(request):
    bucket = Bucket(request)
    for item in bucket:
        item['update_quantity_form'] = BucketAddProductForm(initial={'quantity': item['quantity'],
                                                                     'update': True})
    return render(request, 'bucket/detail.html', {'bucket': bucket})
