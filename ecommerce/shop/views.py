from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def allcategories(request):
    c=Category.objects.all()
    context={'cat':c}

    return render(request,'category.html',context)

def details(request,p):
    k=Product.objects.get(id=p)
    context={'details':k}
    return render(request,'details.html',context)

def allproducts(request,p):                                      #here p is recevies the cateory id
    c=Category.objects.get(id=p)                                 #reads a particular category object using id
    p=Product.objects.filter(category=c)                         #reads all product under a particular category object
    context={'cat':c,'product':p}
    return render(request,'product.html',context)


from django.db.models import Q

def searchbooks(request):
    k=None                         #initialize k as None(no value)
    if(request.method=="POST"):
        query=request.POST['q']    #get input key from form
        if query:
            k=Category.objects.filter(Q(title__icontains=query) | Q(price__icontains=query))    #it checks the key in title and author field.
            #filter funtion returns only the matching records., icontains-->anywhere inside the field,   i--->caseinsensive{uppercase and lower case select}
    return render(request,'search.html',{'search':k})

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']

        if(p==cp):
            u=User.objects.create_user(username=u,password=p,first_name=f,last_name=l,email=e)
            u.save()
            return redirect('shop:categories')

    return render(request,'register.html',)
def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        print(u,p)
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:categories')
        else:
            messages.error(request,'invalid credentials')
            # message display on same page
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect('shop:categories')
def add_categories(request):
    if (request.method == "POST"):
        n = request.POST['n']
        i = request.FILES.get('i')
        d = request.POST['d']
        c=Category.objects.create(name=n,image=i,desc=d)
        c.save()
        return redirect('shop:categories')
    return render(request,'add_categories.html')


def add_product(request):
    if (request.method == "POST"):
        n = request.POST['n']
        i = request.FILES.get('i')
        d = request.POST['d']
        s = request.POST['s']
        p = request.POST['p']
        c = request.POST['c']

        cat=Category.objects.get(name=c)
        c=Product.objects.create(name=n,image=i,desc=d,stock=s,price=p,category=cat)
        c.save()
        return redirect('shop:categories')
    return render(request,'add_product.html')


def add_stock(request,p):
    product=Product.objects.get(id=p)
    if (request.method == "POST"):
        product.stock=request.POST['s']
        product.save()
        return redirect('shop:categories')
    context={'pro':product}
    return render(request,'add_stock.html',context)


