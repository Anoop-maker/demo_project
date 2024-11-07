from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

# Create your views here.
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)   #product-ne eduthitt pinned delete cheyyan
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)                        #defualt-aayi 1 set cheyyan
    date_added=models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.price*self.quantity

class Order_details(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # product-ne eduthitt pinned delete cheyyan
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_items=models.IntegerField()
    address=models.TextField()
    phone=models.IntegerField()
    pin=models.IntegerField()

    order_id=models.CharField(max_length=20,blank=True)
    order_date=models.DateTimeField(auto_now_add=True)

    payment_status=models.CharField(max_length=20,default='pending')
    delivery_status=models.CharField(max_length=20,default='pending')

class Payment(models.Model):
    name=models.CharField(max_length=100)
    amount=models.IntegerField()
    order_id=models.CharField(max_length=30,blank=True)
    razorpay_payment_id=models.CharField(max_length=20,blank=True)
    paid=models.BooleanField(default=False)