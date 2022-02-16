from http.client import HTTPResponse
from itertools import product
from unicodedata import category
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from .forms import CustomerRegistrationForm
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
# from django.db.models import Q
# from django.http import JsonResponse

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDeatilView(View):
    def get(self, request, pk):
        product=Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',{'product':product})


@login_required
def add_to_cart(request):
    # if request.user.is_authenticated:        
        user = request.user
        product_id=request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart')
    # return redirect('accounts/login/')    

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart=Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        card_product = [p for p in Cart.objects.all() if p.user == user]
        if card_product:
            for p in card_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount+shipping_amount
            return render(request, 'app/addtocart.html',{'cart':cart,'totalamount':totalamount,'amount':amount})

# def plus_cart(request):
#     if request.metthod == 'GET':
#         prod_id = request.GET['prod_id']
#         c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity+=1
#         c.save()
#         amount = 0.0
#         shipping_amount = 70.0
#         card_product = [p for p in Cart.objects.all() if p.user == request.user]
#         for p in card_product:
#             tempamount = (p.quantity * p.product.discounted_price)
#             amount += tempamount
#             totalamount = amount+shipping_amount

#         data = {
#             'quantity':c.quqntity,
#             'amount':amount,
#             'totalamount':totalamount
#             }
#         return JsonResponse(data)


@login_required
def buy_now(request):    
    return render(request, 'app/buynow.html')


def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    print(custid)
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity = c.quantity).save()
        c.delete()
    return redirect("orders")


def mobile(request, data=None):
    if data == None: 
        mobiles = Product.objects.filter(category='M')
    return render(request, 'app/mobile.html', {'mobiles' : mobiles})

def login(request):
 return render(request, 'app/login.html')


class customerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self, request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation! Registerd Successfully!!')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items =  Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    card_product = [p for p in Cart.objects.all() if p.user == request.user]
    if card_product:
        for p in card_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})
  