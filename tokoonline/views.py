from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from store.models import Product
import anthropic
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
        data = json.loads(request.body)
        user_message = data.get('message', '')

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            system="""Kamu adalah asisten toko sepatu online bernama Shoespark. 
            Kamu membantu pelanggan menemukan sepatu yang tepat, menjawab pertanyaan 
            tentang produk, harga, pengiriman, dan kebijakan toko. 
            Jawab dengan ramah dan singkat dalam Bahasa Indonesia.""",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return JsonResponse({
            'response': message.content[0].text
        })

    return JsonResponse({'error': 'Method not allowed'}, status=405)