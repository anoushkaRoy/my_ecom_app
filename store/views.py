from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor, Product, Customer, Order, Wishlist, Profile, CustomUser, Cart, CartItem, OrderItem
from .forms import VendorSignUpForm, CustomerSignUpForm, ReviewForm, AddressForm, ProductForm
import requests
from django.conf import settings
from mailjet_rest import Client
from django.http import JsonResponse
import json  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import views as auth_views
import pandas as pd
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.


#home page

def home(request):
    count = User.objects.count()
    return render(request, 'home.html', {
        'count': count
    })




from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            return redirect_based_on_role(request)  # Call a function to determine the redirect URL based on the user's role

        else:
            # Authentication failed, display an error message
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})

    else:
        # Render the login page
        return render(request, 'login.html')




#vendor home page

def vendor_home(request):
    vendor = Vendor.objects.get_or_create(user=request.user)
    context = {
        'vendor': vendor
    }
    return render(request, 'vendor_home.html', context)




#vendor profile page

def vendor_profile(request):
    vendor = Vendor.objects.get_or_create(user=request.user)
    items = Product.objects.filter(vendor=vendor)
    context = {
        'vendor': vendor,
        'items': items
    }
    return render(request, 'vendor_profile.html', context)



#customer home page

def customer_home(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = Order.objects.filter(customer=customer)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, pk=order_id, customer=customer)
            review = form.save(commit=False)
            review.order = order
            review.customer = customer
            review.save()
            return redirect('customer_profile', customer_id=customer_id)
    else:
        form = ReviewForm()

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_profile', customer_id=customer_id)
    else:
        form = AddressForm(instance=customer)


    context = {
        'customer': customer,
        'orders': orders,
        'form': form
    }
    return render(request, 'customer_home.html', context)



#customer orders

def customer_orders(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = Order.objects.filter(customer=customer)
    context = {
        'customer': customer,
        'orders': orders
    }
    return render(request, 'customer_orders.html', context)



#customer add money

def add_money(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        customer.balance += amount
        customer.save()
        return redirect('customer_home', customer_id=customer_id)
    return render(request, 'customer_home.html')



#store page

def store(request,customer_id):

    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, pk=customer_id)
        order, created =Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        wishlistItems=order.get_wishlist_items
    else:
        items= []
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']

    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems,'wishlistItems':wishlistItems}
    return render(request,'store/store.html',context) 



#cart page

def cart(request):

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created =Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items= []
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)



#add to wishlist 

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('wishlist')
    


#wishlist

def wishlist(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created =Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        wishlist_items = order.get_wishlist_items
    else:
        items=[]
        order={'get_wishlist_items':0}
        wishlistItems=order['get_wishlist_items']
    context={'items':items,'order':order,'wishlistItems':wishlistItems}
    return render(request,'store/cart.html',context)



#checkout page

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created =Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items= []
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)


#vendor update item

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']

    print('Action:',action)
    print('productId:',productId)

    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity=(orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('item was added',safe=False)



#redirect based on vendor/customer

def redirect_based_on_role(request):
    if request.user.is_authenticated:
        if Profile.is_customer:
            # Redirect the vendor to the vendor home page
            return redirect('store')
        else:
            # Redirect the customer to the store page
            return redirect('home')
    


#vendor signup page

def vendor_signup(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_vendor = True
            user.save()
            return redirect('home')  # Redirect to vendor's home page
    else:
        form = VendorSignUpForm()
    return render(request, 'registration/vendor_signup.html', {'form': form})



#vendor signup page

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')  # Redirect to the store page
    else:
        form = CustomerSignUpForm()
    return render(request, 'registration/customer_signup.html', {'form': form})



#vendor add item

def add_item(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    if request.method == 'POST':
        item_name = request.POST['item_name']
        item_price = request.POST['item_price']
        Product.objects.create(vendor=vendor, name=item_name, price=item_price)
        return redirect('vendor_items', vendor_id=vendor_id)
    return render(request, 'vendor_home.html')


#vendor delete item

def delete_item(request, item_id):
    item = get_object_or_404(Product, id=item_id, vendor=request.user.vendor)
    
    if request.method == 'POST':
        item.delete()
        return redirect('vendor_items')  # Redirect to the vendor's items list
        
    return render(request, 'delete_item.html', {'item': item})



# customer place order- cannot place order if not enough money or item out of stock

def place_order(request, product_id):
    item = get_object_or_404(Product, pk=product_id)
    customer = request.user.customer
    
    if customer.balance < item.price:
        error_message = "Insufficient funds. Please add money to your account."
    elif item.stock <= 0:
        error_message = "Product is out of stock."
    else:
        # Process the order
        # Deduct the item price from customer's balance
        customer.balance -= item.price
        customer.save()

        # Update the item stock
        item.stock -= 1
        item.save()

        # Create the order
        order = Order.objects.create(customer=customer, item=item)

        success_message = "Order placed successfully."

        api_key = "YOUR_MAILJET_API_KEY"
        api_secret = "YOUR_MAILJET_API_SECRET"
        vendor_email = "vendor@example.com"
        customer_name = "John Doe"
        product_name = "Example Product"

        send_email(api_key, api_secret, vendor_email, customer_name, product_name)

        context = {
            'item': item,
            'success_message': success_message,
        }
        return render(request, 'your_app/order_success.html', context)

    context = {
        'item': item,
        'error_message': error_message,
    }
    return render(request, 'your_app/order_failure.html', context)



#order detail

def order_detail(request):
    customer=request.user.customer
    order, created =Order.objects.get_or_create(customer=customer,complete=False)
    context = {'order': order}
    return render(request, 'order_detail.html', context)



#vendor generate sales report

def generate_sales_report(request):
    # Retrieve sales data related to the vendor
    vendor = request.user.vendor  # Assuming you have a 'vendor' foreign key in the User model
    sales = Order.objects.filter(vendor=vendor)

    # Create a pandas DataFrame with the sales data
    sales_data = []
    for sale in sales:
        sale_info = {
            'Order ID': sale.id,
            'Customer Name': sale.customer.name,
            'Product': sale.product.name,
            'Quantity': sale.quantity,
            'Total Price': sale.get_total_price,
            'Date Ordered': sale.date_ordered,
        }
        sales_data.append(sale_info)
    sales_df = pd.DataFrame(sales_data)

    # Generate the CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    sales_df.to_csv(path_or_buf=response, index=False)

    return response



#new purchase email to vendor

def send_email(api_key, api_secret, vendor_email, customer_name, product_name):
    url = "https://api.mailjet.com/v3.1/send"
    headers = {"Content-Type": "application/json"}

    payload = {
        "Messages": [
            {
                "From": {"Email": "your_email@example.com", "Name": "Your Name"},
                "To": [{"Email": vendor_email, "Name": "Vendor"}],
                "Subject": "New Purchase Notification",
                "TextPart": f"Hello, Vendor!\n\nYou have received a new purchase for the product: {product_name}.\n\nCustomer Name: {customer_name}",
            }
        ]
    }

    response = requests.post(
        url,
        auth=(api_key, api_secret),
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Status code: {response.status_code}")



#move to cart from wishlist

def move_to_cart(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Create a new CartItem and copy the details from the Wishlist item
    CartItem.objects.create(cart=cart, product=wishlist_item.product, quantity=1)

    # Delete the item from the Wishlist
    wishlist_item.delete()

    return redirect('your_app_name:cart')  # Redirect to the cart page



#vendor edit item

def edit_item(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', item_id=item_id)  # Redirect to item detail page
    else:
        form = ProductForm(instance=item)
    
    return render(request, 'edit_item.html', {'form': form, 'item': item})


