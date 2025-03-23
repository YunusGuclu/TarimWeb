from django.urls import path
from .views import home,tarimfiyatlari,about, contact, tarimverileri


urlpatterns = [
    path('', home, name='home'),
    path('tarimfiyatlari/', tarimfiyatlari, name='tarimfiyatlari'),
    path('hakkinda/', about, name='about'),
    path('iletisim/', contact, name='contact'),
    path('tarimverileri/', tarimverileri, name='tarimverileri'),
   

]
