from django.shortcuts import render
from .forms import OrderCreateForm
from .models import OrderItem
from bucket.bucket import Bucket


def order_create(request):
    bucket = Bucket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in bucket:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            bucket.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form, 'bucket': bucket})