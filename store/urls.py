from django.urls import path,include
from . import views
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import wishlist,generate_sales_report



urlpatterns=[
    path('store/',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('',views.home,name='home'),
    path('signup/vendor/', views.vendor_signup, name='vendor_signup'),
    path('signup/customer/', views.customer_signup, name='customer_signup'),
    path('accounts/login/', views.login_view, name='login_view'),
    path('order/', views.order_detail, name='order_detail'),

    path('accounts/profile/', views.redirect_based_on_role, name='redirect_based_on_role'),





    path('customer/home/<int:customer_id>/', views.customer_home, name='customer_home'),
    path('customer/add-money/<int:customer_id>/', views.add_money, name='add_money'),
    path('customer/orders/<int:customer_id>/', views.customer_orders, name='customer_orders'),

    path('place_order/<int:item_id>/', views.place_order, name='place_order'),
    
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(),name='logout'),
    


    path('items/<int:item_id>/edit/', views.edit_item, name='edit_item'),







    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/<int:wishlist_id>/move-to-cart/', views.move_to_cart, name='move_to_cart'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('vendor/home/', views.vendor_home, name='vendor_home'),
    path('vendor/profile/', views.vendor_profile, name='vendor_profile'),
    path('vendor/item/delete/', views.delete_item, name='delete_item'),
    path('vendor/item/add/', views.add_item, name='add_item'),
    path('sales-report/', generate_sales_report, name='sales_report'),
]

    
