from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from store.models import Product
from openai import OpenAI
import json

def index(request):
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Ambil semua produk dari database
            products = Product.objects.filter(is_available=True)
            product_list = ""
            for p in products:
                product_list += f"- {p.name} | Harga: Rp{p.price:,} | Kategori: {str(p.category)} | Stok: {p.stock}\n"

            if not product_list:
                product_list = "Tidak ada produk tersedia saat ini."

            # Koneksi ke DeepSeek
            client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com"
            )

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": f"""Kamu adalah asisten toko sepatu online bernama Shoespark.
Berikut adalah daftar produk yang tersedia di toko kami:

{product_list}

Tugasmu adalah membantu pelanggan menemukan sepatu yang tepat berdasarkan daftar produk di atas.
Jika pelanggan minta rekomendasi, rekomendasikan produk dari daftar di atas beserta harganya.
Jawab dengan ramah dan singkat dalam Bahasa Indonesia."""
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                max_tokens=500,
            )

            return JsonResponse({
                'response': response.choices[0].message.content
            })

        except Exception as e:
            print(f"Chatbot error: {e}")
            return JsonResponse({
                'response': f'Error: {str(e)}'
            }, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)