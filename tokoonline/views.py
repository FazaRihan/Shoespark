from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from store.models import Product
import google.generativeai as genai
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

            # Konfigurasi Gemini
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="""Kamu adalah asisten toko sepatu online 
                bernama Shoespark. Kamu membantu pelanggan menemukan sepatu 
                yang tepat, menjawab pertanyaan tentang produk, harga, 
                pengiriman, dan kebijakan toko. 
                Jawab dengan ramah dan singkat dalam Bahasa Indonesia."""
            )

            response = model.generate_content(user_message)

            return JsonResponse({
                'response': response.text
            })

        except Exception as e:
            return JsonResponse({
                'response': 'Maaf, saya sedang tidak bisa menjawab. Coba lagi!'
            }, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)