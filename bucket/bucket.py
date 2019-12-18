from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Bucket(object):

    def __init__(self, request):
        self.session = request.session
        bucket = self.session.get(settings.BUCKET_SESSION_ID)
        if not bucket:
            bucket = self.session[settings.BUCKET_SESSION_ID] = {}
        self.bucket = bucket

    def __iter__(self):
        product_ids = self.bucket.keys()
        products = Product.objects.filter(id__in=product_ids)

        bucket = self.bucket.copy()
        for product in products:
            bucket[str(product.id)]['product'] = product

        for item in bucket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.bucket.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.bucket:
            self.bucket[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.bucket[product_id]['quantity'] = quantity
        else:
            self.bucket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.bucket:
            del self.bucket[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price'] * item['quantity']) for item in self.bucket.values())

    def clear(self):
        del self.session[settings.BUCKET_SESSION_ID]
        self.save()


