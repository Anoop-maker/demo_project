from cart.models import Cart

def count_items(requeset):
    u=requeset.user
    count=0
    if requeset.user.is_authenticated:
        try:
            c=Cart.objects.filter(user=u)
            for i in c:
                count+=i.quantity

        except:
            count=0

    return {'c':count}

