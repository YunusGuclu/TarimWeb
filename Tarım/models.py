from django.db import models
from django.utils import timezone

class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"

class AgricultureNews(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    url = models.URLField()
    image_url = models.URLField(blank=True, null=True)  

    def __str__(self):
        return self.title

class CommodityPrice(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    change_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    high_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    low_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price} TL"

    class Meta:
        ordering = ['-date']