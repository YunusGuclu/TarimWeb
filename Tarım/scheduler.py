from .utils import get_all_cities_weather, get_agriculture_news
from .models import Weather, AgricultureNews
from apscheduler.schedulers.background import BackgroundScheduler  # Scheduler'ı içe aktarıyoruz

def fetch_weather_data():
    # Türkiye'deki tüm illerin listesi
    cities = [
        "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", 
        "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", 
        "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", 
        "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", 
        "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman", 
        "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir", "Kilis", "Kocaeli", "Konya", 
        "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", 
        "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Şanlıurfa", "Şırnak", 
        "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"
    ]

    weather_data = get_all_cities_weather(cities)

    for weather in weather_data:
        Weather.objects.update_or_create(
            city=weather["city"],
            defaults={
                "temperature": weather["temperature"],
                "description": weather["description"],
                "icon": weather["icon"],
            }
        )

def fetch_agriculture_news():
    news_data = get_agriculture_news()

    for news in news_data:
        AgricultureNews.objects.update_or_create(
            title=news["title"],
            defaults={
                "description": news["description"],
                "published_at": news["published_at"],
                "url": news["url"],
                "image_url": news["image"],
            }
        )


# ... mevcut importlar ...

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Aralıkları artırıyoruz
    scheduler.add_job(fetch_weather_data, 'interval', minutes=5)  # 1 dakika yerine 5 dakika
    scheduler.add_job(fetch_agriculture_news, 'interval', minutes=10)  # 1 dakika yerine 10 dakika
    
    
    scheduler.start()
