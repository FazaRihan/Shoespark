from django.contrib import admin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display        = ('name', 'slug')
    # list_display_links = ('email', 'first_name', 'last_name')
    # readonly_fields = ('last_login', 'date_joined',)
    # ordering = ('-date_joined',) # add minus sign (-) to make it Descending
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Category, CategoryAdmin)