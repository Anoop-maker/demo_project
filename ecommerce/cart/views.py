from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from shop.models import Product
from cart.models import Cart,Payment,Order_details
from django.contrib.auth.models import User
import razorpay
@login_required
def cart(request,i):
    p=Product.objects.get(id=i)
    u=request.user

    try:
        c=Cart.objects.get(user=u,product=p)  #check the product present in the cart table from particular user
        c.quantity+=1                         #if present it will increment the quantity of product
        c.save()
        p.stock-=1                            #decrese stock to adding cart
        p.save()
    except:                                   #if not present then it will create a new record inside the class table with quantity =1
        c=Cart.objects.create(product=p,user=u,quantity=1)
        c.save()
        p.stock -= 1
        p.save()

    return redirect('cart:cart_view')


@login_required
def cart_view(request):
    u=request.user

    total=0
    c=Cart.objects.filter(user=u)              #all cart items for a particular user

    for i in c:
        total+=i.quantity * i.product.price      #calculate the sum of each product and price
    context={'cart':c,'total':total}
    return render(request,'cart.html',context)


def cart_remove(request,i):
    p=Product.objects.get(id=i)
    u=request.user

    try:
        c=Cart.objects.get(user=u,product=p)
        if(c.quantity>1):
            c.quantity-=1
            c.save()
            p.stock+=1
            p.save()
        else:
            c.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return redirect('cart:cart_view')


@login_required
def cart_delete(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        k=Cart.objects.get(user=u,product=p)
        k.delete()
        p.stock += k.quantity
        p.save()
    except:
        pass
    return redirect('cart:cart_view')

@login_required
def order_form(request):

    if(request.method=='POST'):
        address=request.POST['a']
        phone=request.POST['p']
        pin=request.POST['pi']
        u=request.user

        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total+=i.quantity*i.product.price
        total=int(total*100)
        client=razorpay.Client(auth=('rzp_test_KOGbLoyyMNz5XN','QxSQ85OLqkilkiDkMAQ7JLvn'))         #create a client connection with razorpay
        # using razorpay id and secret code

        response_payment=client.order.create(dict(amount=total,currency='INR'))   # create an order with
        # razorpay using razorpay client
        # print(response_payment)

        order_id=response_payment['id']          #retrieves the order_id from response
        order_status=response_payment['status']  #retrieves status from response
        if(order_status=='created'):             #if status is created then store order_id in Payment and Order_details table
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()

            for i in c:                          #for each item created a recored inside Order_details table
                o=Order_details.objects.create(product=i.product,user=u,no_of_items=i.quantity,address=address,phone=phone,order_id=order_id,pin=pin)
                o.save()
        else:
            pass

        response_payment['name'] = u.username
        context = {'payment': response_payment}
        return render(request,'payment.html',context)

    return render(request,'order_form.html')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def payment_status(request,u):

    user = User.objects.get(username=u)        # user name get cheythu
    if(not request.user.is_authenticated):     # if user is not authenticated
        login(request,user)                    # allowing request user to login

    if(request.method=='POST'):
        response=request.POST                  #deictionary success aanel payment id and order details
        print(response)


        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }

        client=razorpay.Client(auth=('rzp_test_KOGbLoyyMNz5XN','QxSQ85OLqkilkiDkMAQ7JLvn'))
        print(client)
        try:
            status=client.utility.verify_payment_signature(param_dict)    #verificatin:-to check the authrnticaticity of rhe razorpay signature
            print(status)

            #to retrive the oaarticular record in payment table whose order isd matches the response order id  (table data adding)
            p=Payment.objects.get(order_id=response['razorpay_order_id'])
            p.razorpay_payment_id=response['razorpay_payment_id']        # adds the payment id after successful payment
            p.paid=True                                                  #checnge the paid status true
            p.save()


            o=Order_details.objects.filter(user=user,order_id=response['razorpay_order_id'])  #retrive the particular record in order_details
            #matching with current user and response order_id
            for i in o:
                i.payment_status='Paid'
                i.save()

            c=Cart.objects.filter(user=user)     #user selected cart delete after success
            c.delete()


        except:
            pass

    return render(request,'payment_status.html',{'status':status})

@login_required()
def your_orders(request):
    u=request.user
    d=Order_details.objects.filter(user=u,payment_status='Paid')         #payment status paid aaya details eduthaal mathy
    context={'orders':d}

    return render(request,'your_orders.html',context)

