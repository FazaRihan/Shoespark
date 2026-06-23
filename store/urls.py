from django.urls import path
from . import views

urlpatterns = [

    # ─── URL Halaman Biasa ─────────────────────────────────
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('admin-panel/', views.custom_dashboard, name='custom_dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ─── REST API ──────────────────────────────────────────
    path('api/products/', views.api_product_list, name='api_product_list'),
    path('api/products/new/', views.api_new_arrivals, name='api_new_arrivals'),
    path('api/products/search/', views.api_search, name='api_search'),
    path('api/products/<int:pk>/', views.api_product_detail, name='api_product_detail'),
    path('api/products/<int:pk>/variations/', views.api_product_variations, name='api_product_variations'),
    path('api/products/category/<slug:category_slug>/', views.api_products_by_category, name='api_products_by_category'),
    path('api/categories/', views.api_category_list, name='api_category_list'),

]