from .models import Item, Cart
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    all_items = Item.objects.all()
    if not request.user.is_authenticated:
        print('No one inside the app')
        num_items_in_cart = 0
        return render(request, 'cart/index.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})
    else:
        user = request.user
        num_items_in_cart = user.profile.cart_items.all().count()
        return render(request, 'cart/index.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})

def itemlist(request):
    all_items = Item.objects.all()
    user = request.user
    if not user.is_authenticated:
        num_items_in_cart=0
        return render(request, 'cart/itemlist.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})
    num_items_in_cart=user.profile.cart_items.all().count()
    return render(request, 'cart/itemlist.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})

def shoppingcart(request):
    user = request.user
    print("Hey Dude")
    if not user.is_authenticated:
        num_items_in_cart=0
        return render(request, 'cart/shopping-cart.html', {'num_items_in_cart': num_items_in_cart})
    all_user_items = user.profile.cart_items.all()
    print(all_user_items)
    tot_cost = 0
    for i in all_user_items:
        print(i.quantity)
        tot_cost += i.itemtotal
    print(tot_cost)
    num_items_in_cart=user.profile.cart_items.all().count()
    return render(request, 'cart/shopping-cart.html', {'num_items_in_cart': num_items_in_cart, 'all_user_items': all_user_items, 'tot_cost': tot_cost})

def search(request):
    print(request.method)
    if request.method == 'POST':
        itemname = request.POST.get('itemname')
        print(itemname)
        item_obj = Item.objects.filter(name=itemname)
        print(item_obj[0].price)
        num_items_in_cart = item_obj.count()
        context = {'all_items': item_obj , 'num_items_in_cart': num_items_in_cart}
        return render(request, 'cart/product_card.html', context)


def searchpage(request):
    all_items = Item.objects.all()
    user = request.user
    if not user.is_authenticated:
        num_items_in_cart=0
        context = {'all_items': all_items , 'num_items_in_cart': num_items_in_cart, 'order_active': 'active'}
        return render(request, 'cart/product_card.html', context)
    paginator = Paginator(all_items, 4)
    page = request.GET.get('page')
    all_items = paginator.get_page(page)
    # paginate_by = 2
    num_items_in_cart = user.profile.cart_items.all().count()
    context = {'all_items': all_items , 'num_items_in_cart': num_items_in_cart, 'order_active': 'active'}
    return render(request, 'cart/product_card.html', context)

def product_page(request, Id):
    item = get_object_or_404(Item, id=Id)
    user = request.user
    num_items_in_cart = user.profile.cart_items.all().count()
    return render(request, 'cart/product_page.html', {'num_items_in_cart':num_items_in_cart, 'item':item})

def add_to_cart(request, Item_id):
    item = get_object_or_404(Item, id=Item_id)
    check=0
    user = request.user
    if not user.is_authenticated:
        return redirect('user:register')
    for obj in user.profile.cart_items.all():
        if obj.item.id == item.id:
            obj.quantity=obj.quantity+1
            obj.itemtotal=(item.price)*float(obj.quantity)
            obj.save()
            check=1
    if check==0:
        temp=Cart()
        temp.item=item
        temp.quantity=1
        temp.itemtotal=(item.price)*float(temp.quantity)
        temp.save()
        user.save()
        user.profile.cart_items.add(temp)
        user.save()
        print(user.profile.cart_items.all())
    all_user_items = user.profile.cart_items.all()
    all_items = Item.objects.all()
    num_items_in_cart = user.profile.cart_items.all().count()
    tot_cost=0
    for i in all_user_items:
        print(i.quantity)
        tot_cost += i.itemtotal
    print(tot_cost)
    # return render(request, 'cart/product_card.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})
    return render(request, 'cart/shopping-cart.html', {'all_user_items': all_user_items ,'user':user,'num_items_in_cart':num_items_in_cart, 'tot_cost': tot_cost})

def add_single_item_into_cart(request, Item_id):
    item = get_object_or_404(Item, id=Item_id)
    user = request.user
    for obj in user.profile.cart_items.all():
        if obj.item.id == item.id:
            obj.quantity+=1
            obj.itemtotal=(item.price)*float(obj.quantity)
            obj.save()
    return redirect('cart:shoppingcart')

def remove_from_cart(request, Item_id):
    item = get_object_or_404(Item, id=Item_id)
    user = request.user
    for obj in user.profile.cart_items.all():
        if obj.item.id == item.id:
            user.profile.cart_items.filter(id=obj.id ).delete()
    return redirect('cart:shoppingcart')


def remove_single_item_from_cart(request, Item_id):
    item = get_object_or_404(Item, id=Item_id)
    user = request.user
    for obj in user.profile.cart_items.all():
        if obj.item.id == item.id:
            if obj.quantity>1:
                obj.quantity-=1
                obj.itemtotal=(item.price)*float(obj.quantity)
                obj.save()
            else:
                user.profile.cart_items.filter(id=obj.id).delete()
    return redirect('cart:shoppingcart')


def checkout(request):
    user = request.user
    if not user.is_authenticated:
        num_items_in_cart=0
        return render(request, 'cart/payment.html', {'num_items_in_cart': num_items_in_cart})
    
    num_items_in_cart = user.profile.cart_items.all().count()
    return render(request, 'cart/payment.html', {'num_items_in_cart': num_items_in_cart})
