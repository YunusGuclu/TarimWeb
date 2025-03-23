import json
from pathlib import Path
from Tarım.models import Product  # Modelinizi doğru yolla içe aktarın

def import_json_to_model():
    # JSON dosyasının yolu
    json_file_path = Path(__file__).resolve().parent / 'Json' / 'fiyat.json'

    # JSON dosyasını aç ve yükle
    with open(json_file_path, encoding="utf-8") as file:
        data = json.load(file)

    # JSON verilerini modele aktar
    for item in data:
        name = item.get("Name")
        price = item.get("2023").replace(",", ".")  # Virgül ayracını noktaya çevir

        # Modelde yeni bir ürün oluştur
        Product.objects.create(name=name, price_2023=price)

    print("JSON verileri başarıyla modele aktarıldı!")
