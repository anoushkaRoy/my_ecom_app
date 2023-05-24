from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Review

class VendorSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2',)  # Customize fields as per your requirements

class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2',)  # Customize fields as per your requirements


from django import forms
from .models import Customer

class AddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']  # Add any other fields as needed

