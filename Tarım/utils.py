import requests
from bs4 import BeautifulSoup
import json
import http.client
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
import yfinance as yf
import time
from django.utils import timezone 

def get_weather(city):
    api_key = 'c45966f73686cf713980007192a3b8aa'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=tr"  

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        weather = {
            "city": city,  
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
        return weather

    except requests.exceptions.HTTPError as err:
        print(f"Hava durumu API hatası: {err}")
        return None

def get_all_cities_weather(cities):
    weather_data = []
    for city in cities:
        weather = get_weather(city)
        if weather:
            weather_data.append(weather)
    return weather_data


def get_agriculture_news():
    api_key = '73078443d44f4fc9b292370fe3a0f98b'
    url = f'https://newsapi.org/v2/everything?q=tarım OR tarımsal&language=tr&sortBy=publishedAt&apiKey={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get('articles', [])

        news_list = []
        for article in articles:
            image_url = article.get("urlToImage", "")

            if 'tarım' in article['title'].lower() or 'tarım' in (article.get('description') or '').lower():
                news_item = {
                    "title": article["title"],
                    "description": article.get("description", ""),
                    "published_at": article["publishedAt"],
                    "url": article["url"],
                    "image": image_url if image_url else "https://example.com/default_image.jpg"  # Varsayılan resim ekle
                }
                news_list.append(news_item)
        return news_list

    except requests.exceptions.HTTPError as err:
        print(f"NewsAPI hatası: {err}")
        return None
    

def get_tmo_data():
    url = "https://www.tmo.gov.tr/alim-fiyatlari"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print("TMO verileri çekiliyor...")
        response = requests.get(url, headers=headers, verify=False)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            print("HTML içeriği alındı")
            
            # Fiyat tablosunu bul
            table = soup.find('table', {'class': 'table'})
            if not table:
                print("Fiyat tablosu bulunamadı!")
                return None
            
            data = []
            rows = table.find_all('tr')[1:]  # Başlık satırını atla
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    try:
                        # Fiyat metnini temizle ve sayıya çevir
                        price_text = cols[1].text.strip().replace('.', '').replace(',', '.').replace('TL', '').strip()
                        price = float(price_text) if price_text else 0.0
                        
                        product = {
                            'name': cols[0].text.strip(),
                            'price': price,
                            'date': cols[2].text.strip() if len(cols) > 2 else ''
                        }
                        print(f"Ürün eklendi: {product}")
                        data.append(product)
                    except ValueError as ve:
                        print(f"Fiyat dönüştürme hatası: {ve}")
                        continue
            
            return data
            
    except Exception as e:
        print(f"TMO veri çekme hatası: {e}")
        return None

# Alternatif veri kaynağı: Ticaret Bakanlığı Hal Fiyatları
def get_hal_fiyatlari():
    url = "https://www.ticaret.gov.tr/istatistikler/hal-fiyatlari"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print("Hal fiyatları çekiliyor...")
        response = requests.get(url, headers=headers, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Fiyat tablosunu bul
            table = soup.find('table', {'class': 'table'})
            if not table:
                print("Hal fiyatları tablosu bulunamadı!")
                return None
            
            data = []
            rows = table.find_all('tr')[1:]  # Başlık satırını atla
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    try:
                        price_text = cols[2].text.strip().replace('.', '').replace(',', '.').replace('TL', '').strip()
                        price = float(price_text) if price_text else 0.0
                        
                        product = {
                            'name': cols[0].text.strip(),
                            'price': price,
                            'date': cols[1].text.strip() if len(cols) > 1 else ''
                        }
                        data.append(product)
                    except ValueError:
                        continue
            
            return data
            
    except Exception as e:
        print(f"Hal fiyatları veri çekme hatası: {e}")
        return None

from .models import CommodityPrice  # Bu import'u en üste ekleyin

def get_us_agriculture_data():
    try:
        # SSL uyarılarını kapat
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # GERÇEKTEN veri çekilebilenler (27.03.2024)
        commodities = {
            # ETF'ler (Çalışanlar)
            'CORN': 'Mısır ETF',       # Teucrium Corn Fund - ÇALIŞIYOR
            'WEAT': 'Buğday ETF',      # Teucrium Wheat Fund - ÇALIŞIYOR
            'SOYB': 'Soya ETF',        # Teucrium Soybean Fund - ÇALIŞIYOR
            'DBA': 'Tarım ETF',        # Invesco DB Agriculture Fund - ÇALIŞIYOR
            'MOO': 'VanEck Agribusiness ETF',  # VanEck Vectors Agribusiness ETF - ÇALIŞIYOR
            'VEGI': 'Gıda ETF',        # iShares MSCI Global Agriculture - ÇALIŞIYOR
            'TAGS': 'Tarım ETF',       # Teucrium Agricultural Fund - ÇALIŞIYOR
            
            # Future Kontratları (Çalışanlar)
            'CT=F': 'Pamuk',           # Cotton Futures - ÇALIŞIYOR
            'SB=F': 'Şeker',           # Sugar Futures - ÇALIŞIYOR
            
            # Hisse Senetleri (Çalışanlar)
            'ADM': 'Archer-Daniels-Midland', # ÇALIŞIYOR
            'DE': 'John Deere',        # ÇALIŞIYOR
            'NTR': 'Nutrien',          # ÇALIŞIYOR
            'CTVA': 'Corteva',         # ÇALIŞIYOR
            'FMC': 'FMC Corp'          # ÇALIŞIYOR
        }
        
        products = []
        saved_count = 0
        print("ABD tarım borsası verileri çekiliyor...")
        
        # USD/TRY kuru için hata yönetimi
        try:
            usd_try = yf.Ticker('USDTRY=X')
            history = usd_try.history(period='1d')
            if not history.empty:
                exchange_rate = float(history['Close'].iloc[-1])
                print(f"Döviz kuru başarıyla alındı: {exchange_rate}")
            else:
                exchange_rate = 31.5
                print("Döviz kuru alınamadı, varsayılan değer kullanılıyor:", exchange_rate)
        except Exception as e:
            print(f"Dolar kuru çekilemedi: {e}")
            exchange_rate = 31.5
            print("Hata nedeniyle varsayılan döviz kuru kullanılıyor:", exchange_rate)
        
        for symbol, name in commodities.items():
            try:
                print(f"{name} verileri çekiliyor...")
                time.sleep(1)  # API limitlerini aşmamak için bekleme
                
                ticker = yf.Ticker(symbol)
                data = ticker.history(period='1d', interval='1d')  # Günlük veri
                
                if not data.empty:
                    price = float(data['Close'].iloc[-1])
                    price_tl = price * exchange_rate
                    
                    # Değişim yüzdesini hesapla
                    if len(data) > 1:
                        prev_price = float(data['Close'].iloc[-2])
                        change_percent = ((price - prev_price) / prev_price) * 100
                    else:
                        change_percent = 0.0
                    
                    # Timezone aware datetime kullan
                    current_time = timezone.now()
                    
                    product_data = {
                        'name': name,
                        'symbol': symbol,
                        'price': round(price_tl, 2),
                        'price_usd': round(price, 2),
                        'change_percent': round(change_percent, 2),
                        'volume': int(data['Volume'].iloc[-1]) if 'Volume' in data else 0,
                        'high': round(float(data['High'].iloc[-1]) * exchange_rate, 2),
                        'low': round(float(data['Low'].iloc[-1]) * exchange_rate, 2),
                        'high_usd': round(float(data['High'].iloc[-1]), 2),
                        'low_usd': round(float(data['Low'].iloc[-1]), 2),
                        'date': current_time
                    }
                    
                    # Veritabanına kaydet
                    commodity = CommodityPrice.objects.create(**product_data)
                    saved_count += 1
                    
                    products.append(product_data)
                    print(f"Başarıyla kaydedildi: {name} - Fiyat: {price_tl:.2f} TL (${price:.2f})")
                else:
                    print(f"Veri alınamadı: {symbol}")
                    
            except Exception as e:
                print(f"Hata ({symbol}): {e}")
                continue
        
        if not products:
            print("Hiç veri alınamadı!")
            return None
        
        # Fiyata göre sırala
        products.sort(key=lambda x: x['price'], reverse=True)
        print(f"Toplam {len(products)} ürün verisi başarıyla çekildi ve {saved_count} ürün veritabanına kaydedildi.")
        return products
        
    except Exception as e:
        print(f"Genel hata: {e}")
        return None