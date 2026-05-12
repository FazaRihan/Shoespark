from .models import Category

# takes a request as an argument and returns a dictionary of data as context variables.
def menu_links(request):
    links = Category.objects.all()
    
    return dict(links=links)