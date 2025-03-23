from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AgricultureNews

@receiver(post_save, sender=AgricultureNews)
def limit_agriculture_news(sender, instance, **kwargs):
    max_news = 50
    news_count = AgricultureNews.objects.count()
    if news_count > max_news:
        # En eski haberleri al
        excess_news = AgricultureNews.objects.all().order_by('published_at')[:news_count - max_news]
        # Her birini teker teker sil
        for news in excess_news:
            news.delete()