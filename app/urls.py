from django.conf import settings
from django.urls import path
from app import views
from .forms import LoginForm, MyPasswordChangeForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(), name='home'),

    path('product-detail/<int:pk>', views.ProductDeatilView.as_view(), name='product-detail'),


    path('cart/', views.show_cart, name='showcart'),
    #  path('pluscart/', views.plus_cart, name='pluscart'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('buy/', views.buy_now, name='buy-now'),
    path('accounts/profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('paymentdone/', views.payment_done, name='paymentdone'),


    path('mobile/', views.mobile, name='mobile'),
    
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'), name='logout'),    
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('checkout/', views.checkout, name='checkout'),
    path('registration/', views.customerRegistrationView.as_view(), name='customerregistration'),
]
