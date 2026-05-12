from django.contrib import admin
from .models import Product, Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display        = ('name', 'slug', 'price', 'stock', 'category_id', 'updated_at', 'is_available') 

class VariationAdmin(admin.ModelAdmin):
    list_display    = ('product', 'variation_category', 'variation_value', 'is_active') 
    list_editable   = ('variation_value', 'is_active',)
    list_filter     = ('product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)