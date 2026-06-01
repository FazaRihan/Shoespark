from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('category/<slug:category_slug>/', views.store, name="products_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name="product_detail"),
    path('search/', views.search, name="search"),
    path('admin-panel/', views.custom_dashboard, name='custom_dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
