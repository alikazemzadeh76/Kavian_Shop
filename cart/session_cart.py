from product.models import Product

CART_SESSION_ID = 'cart'


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(item['price'])
            item['id'] = self.unique_id(product.id, item['color'], item['size'])

            yield item

    def total(self):
        cart = self.cart.values()
        total_price = sum(int(item['price']) * int(item['quantity']) for item in cart)
        return total_price

    def unique_id(self, id, color, size):
        result = f"{id}-{color}-{size}"
        return result

    def add(self, product, color, size, quantity):
        unique = str(self.unique_id(product.id, color, size))
        if unique not in self.cart:
            self.cart[unique] = {'quantity': 0, 'price': product.price, 'color': color, 'size': size, 'id': product.id}

        self.cart[unique]['quantity'] += int(quantity)
        self.save()


    def delete_cart(self):   #این متد برای حذف کامل سبد خرید بعد از اینه که ما محصولاتو میفرستیم برای پرداخت
        del self.session[CART_SESSION_ID]

    def remove(self, id):   # این متد برای حذف محصولات انتخابی از سبد خرید است
        if id in self.cart:
            del self.cart[id]
        self.save()

    def save(self):
        self.session.modified = True
