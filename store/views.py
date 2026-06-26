from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, VariationSerializer, CategorySerializer

from store.models import Product, Variation
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id



# Create your views here.
@staff_member_required(login_url='login') 
def custom_dashboard(request):
    return render(request, 'admin_dashboard.html')

def store(request, category_slug=None):
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    new_arrivals = Product.objects.filter(is_new=True, is_available=True).order_by('-created_at')[:6]
    
    context = {
        'products': paged_products,
        'product_count': product_count,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'store/index.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e
    
    context = {
        'product': product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email     = request.POST.get('email')
        message   = request.POST.get('message')
        messages.success(request, 'Pesan kamu berhasil dikirim!')
        return redirect('contact')
    return render(request, 'contact.html')

# ─── REST API Views ────────────────────────────────────────

@api_view(['GET'])
def api_product_list(request):
    products = Product.objects.filter(is_available=True).order_by('-created_at')
    serializer = ProductSerializer(products, many=True)
    return Response({'count': products.count(), 'results': serializer.data})


@api_view(['GET'])
def api_product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk, is_available=True)
    except Product.DoesNotExist:
        return Response({'error': 'Produk tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def api_product_variations(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Produk tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
    variations = Variation.objects.filter(product=product, is_active=True)
    serializer = VariationSerializer(variations, many=True)
    return Response({'product': product.name, 'variations': serializer.data})


@api_view(['GET'])
def api_new_arrivals(request):
    products = Product.objects.filter(is_new=True, is_available=True).order_by('-created_at')
    serializer = ProductSerializer(products, many=True)
    return Response({'count': products.count(), 'results': serializer.data})


@api_view(['GET'])
def api_products_by_category(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return Response({'error': 'Kategori tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
    products = Product.objects.filter(category=category, is_available=True)
    serializer = ProductSerializer(products, many=True)
    return Response({'category': category.category_name, 'count': products.count(), 'results': serializer.data})


@api_view(['GET'])
def api_search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({'error': 'Parameter ?q= tidak boleh kosong'}, status=status.HTTP_400_BAD_REQUEST)
    products = Product.objects.filter(name__icontains=query, is_available=True)
    serializer = ProductSerializer(products, many=True)
    return Response({'query': query, 'count': products.count(), 'results': serializer.data})


@api_view(['GET'])
def api_category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response({'count': categories.count(), 'results': serializer.data})

import requests
import base64
from django.conf import settings
from django.http import JsonResponse

def image_search(request):
    """Upload gambar sepatu lalu cari produk serupa"""
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

        # Kirim ke Imagga API untuk mendapat tag/keyword
        try:
            response = requests.post(
                'https://api.imagga.com/v2/tags',
                auth=(settings.IMAGGA_API_KEY, settings.IMAGGA_API_SECRET),
                data={'image_base64': image_data}
            )
            result = response.json()
            tags = result.get('result', {}).get('tags', [])

            # Ambil keyword teratas dari hasil Imagga
            keywords = [tag['tag']['en'] for tag in tags[:5]]

            # Cari produk di database yang cocok dengan keyword
            from store.models import Product
            from django.db.models import Q

            products = Product.objects.none()
            for keyword in keywords:
                products = products | Product.objects.filter(
                    Q(name__icontains=keyword) |
                    Q(description__icontains=keyword) |
                    Q(category__category_name__icontains=keyword),
                    is_available=True
                )

            products = products.distinct()

            # Kirim hasil ke template
            context = {
                'products': products,
                'keywords': keywords,
                'total_found': products.count(),
            }
            return render(request, 'store/image_search_results.html', context)

        except Exception as e:
            context = {
                'error': 'Gagal memproses gambar. Coba lagi.',
                'products': [],
            }
            return render(request, 'store/image_search_results.html', context)

    return render(request, 'store/image_search_results.html', {})