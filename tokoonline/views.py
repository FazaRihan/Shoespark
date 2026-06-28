from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from store.models import Product
from google import genai
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

            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"""Kamu adalah asisten toko sepatu online bernama Shoespark. 
                Kamu membantu pelanggan menemukan sepatu yang tepat, menjawab pertanyaan 
                tentang produk, harga, pengiriman, dan kebijakan toko. 
                Jawab dengan ramah dan singkat dalam Bahasa Indonesia.
                
                Pertanyaan pelanggan: {user_message}"""
            )

            return JsonResponse({
                'response': response.text
            })

        except Exception as e:
            print(f"Chatbot error: {e}")
            return JsonResponse({
                'response': 'Maaf, saya sedang tidak bisa menjawab. Coba lagi!'
            }, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)