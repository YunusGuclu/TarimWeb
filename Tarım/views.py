from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Weather, AgricultureNews, CommodityPrice
import pandas as pd
from datetime import datetime, timedelta
import http.client

from .utils import get_weather, get_us_agriculture_data

def home(request):
    # Varsayılan şehir
    default_city = 'Ankara'
    city = request.GET.get('city', default_city)  # Kullanıcıdan şehir al, yoksa varsayılanı kullan
    weather_data = get_weather(city)  # Girilen şehir için hava durumu verisini al
    agriculture_news_list = AgricultureNews.objects.all().order_by('-published_at')  # En yeni haberler ilk sırada

    # Sayfalama ayarları
    paginator = Paginator(agriculture_news_list, 12)  # Sayfa başına 12 haber
    page_number = request.GET.get('page')  # URL'den sayfa numarasını al
    page_obj = paginator.get_page(page_number)  # İlgili sayfayı al

    context = {
        'weather_data': weather_data,
        'agriculture_news': page_obj,  # Sayfaya özel haberler
    }
    return render(request, 'index.html', context)


from django.shortcuts import render
from .models import CommodityPrice
from .utils import get_us_agriculture_data
from django.utils import timezone

def tarimfiyatlari(request):
    try:
        # Mevcut kayıtların sayısını kontrol et
        initial_count = CommodityPrice.objects.count()
        print(f"Başlangıçtaki kayıt sayısı: {initial_count}")

        # US tarım verilerini al (bu fonksiyon zaten veritabanına kaydediyor)
        us_data = get_us_agriculture_data()
        
        if not us_data:
            print("Veri çekilemedi, örnek veriler kullanılıyor...")
            current_time = timezone.now()
            
            products = [
                {'name': 'Buğday', 'symbol': 'ZW=F', 'price': 9850.50, 'price_usd': 312.50, 'change_percent': 1.25, 'volume': 15000, 'high': 9900.00, 'low': 9800.00, 'high_usd': 314.00, 'low_usd': 311.00, 'date': current_time},
                # ... diğer örnek veriler ...
            ]
            is_sample_data = True
        else:
            products = us_data
            is_sample_data = False
            
            # Bu kısmı kaldırıyoruz çünkü get_us_agriculture_data zaten kaydetmiş oluyor
            # try:
            #     for product in products:
            #         CommodityPrice.objects.create(**product)
            # except Exception as e:
            #     print(f"Veritabanı kayıt hatası: {e}")

        # Son kayıt sayısını kontrol et
        final_count = CommodityPrice.objects.count()
        print(f"Son kayıt sayısı: {final_count}")
        print(f"Eklenen kayıt sayısı: {final_count - initial_count}")

        context = {
            'products': products,
            'is_sample_data': is_sample_data,
            'us_count': len(products) if products else 0
        }
        return render(request, 'tarimfiyatlari.html', context)
        
    except Exception as e:
        print(f"Görünüm hatası: {e}")
        return render(request, 'tarimfiyatlari.html', {'products': [], 'is_sample_data': True, 'us_count': 0})
def about(request):
    return render(request, 'about.html')


from django.core.mail import send_mail
from django.http import JsonResponse

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            'Yeni İletişim Mesajı',
            full_message,
            'your-email@example.com',  # Replace with your email
            ['yazilim456@gmail.com'],
            fail_silently=False,
        )
        return JsonResponse({'success': True})

    return render(request, 'contact.html')


def tarimverileri(request):
    return render(request, 'tarimverileri.html')
