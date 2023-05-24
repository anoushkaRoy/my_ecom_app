from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name
    
class Vendor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    

#to check if the user is customer
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_customer = models.BooleanField(default=False)



class CustomUser(AbstractUser):
    is_vendor = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set'  # Add a related_name argument
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set'  # Add a related_name argument
    )

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    digital=models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)
    description = models.TextField(max_length=800,null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    

    def __str__(self):
        return self.name
    
    def get_product_id(self):
        return self.id
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except: 
            url=''
        return url
    
    @property
    def discounted_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price
    

        
class Order(models.Model):
    
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping=True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_wishlist_items(self):
        wishlistitems=self.orderitem_set.all()
        total=sum([item.quantity for item in wishlistitems])
        return total
    

class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity =models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    

class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField()

    def __str__(self):
        return f"Review for Order #{self.order.pk} by {self.customer.user.username}"
    
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.username + "'s Wishlist"




class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you have a Product model
    quantity = models.PositiveIntegerField(default=1)
