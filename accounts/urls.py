from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),

    path('transactions/', views.transactions, name='transactions'),
    path('returns/', views.returns, name='returns'),
    path('settings/', views.settings, name='settings'),
    path('my_selling_items/', views.my_selling_items, name='my_selling_items'),
    path('received_orders/', views.received_orders, name='received_orders'),
    
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('forgotpassword/', views.forgotpassword, name="forgotpassword"),
    path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name="resetpassword_validate"),
    path('resetpassword/', views.resetpassword, name="resetpassword"),
]