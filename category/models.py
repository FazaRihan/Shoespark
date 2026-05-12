from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name        = models.CharField(max_length=255)
    slug        = models.SlugField(unique=True, max_length=255)
    description = models.TextField()
    image       = models.ImageField(upload_to='photos/categories/', blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'   
        
    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])