import sqlite3

# SQLite Veritabanı Oluşturma
conn = sqlite3.connect('tarim_bilgileri.db')
cursor = conn.cursor()

# Tablo Oluşturma
cursor.execute('''
CREATE TABLE IF NOT EXISTS Toprak_Bilgisi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Toprak_Turu TEXT NOT NULL,
    Urunler TEXT NOT NULL,
    Ozellikler TEXT
)
''')

# 20 Çeşit Toprak Türü ve Verileri
veriler = [
    ("Kumlu", "Havuç, Patates, Soğan, Kavun", "Hafif ve iyi drenajlı toprak."),
    ("Killi", "Buğday, Mısır, Pancar, Bezelye", "Su tutma kapasitesi yüksektir."),
    ("Tınlı", "Zeytin, Üzüm, Şeftali, Kayısı", "Dengeli ve verimli toprak."),
    ("Organik", "Marul, Çilek, Domates, Ispanak", "Organik madde bakımından zengin."),
    ("Turba", "Çilek, Fındık, Ahududu", "Organik madde oranı yüksektir."),
    ("Çakıllı", "Lavanta, Kekik, Nane", "Drenajı iyi fakat besin maddesi az."),
    ("Alüvyonlu", "Pamuk, Sebzeler, Mısır", "Verimli ve besin maddesi açısından zengindir."),
    ("Kireçli", "Arpa, Buğday, Nohut", "PH seviyesi yüksektir."),
    ("Siltli", "Mısır, Ayçiçeği, Sebzeler", "İnce taneli ve verimli toprak."),
    ("Podzolik", "Patates, Çay, Orman Bitkileri", "Asidik toprak yapısı."),
    ("Laterit", "Kahve, Pirinç, Muz", "Tropikal bölgelerde bulunur."),
    ("Kahverengi Orman", "Buğday, Çavdar, Mısır", "Organik madde açısından zengindir."),
    ("Kırmızı", "Pamuk, Yerfıstığı, Şeker Kamışı", "Demir oksit oranı yüksektir."),
    ("Tuzlu", "Pirinç, Halofit Bitkiler", "Tuz oranı yüksektir."),
    ("Volkanik", "Kahve, Sebzeler, Meyveler", "Mineral açısından zengin ve verimlidir."),
    ("Taşlı", "Lavanta, Adaçayı, Kekik", "Drenajı çok iyidir."),
    ("Çorak", "Kuraklığa Dayanıklı Bitkiler", "Besin maddesi az ve verimsiz."),
    ("Çamurlu", "Pirinç, Su Bitkileri", "Drenajı zayıf toprak."),
    ("Karstik", "Zeytin, Üzüm, İncir", "Kireç taşlarının bulunduğu bölgelerde görülür."),
    ("Humuslu", "Her Tür Tarım Ürünü", "Çok verimli ve zengin organik madde içerir.")
]

# Verileri Tabloya Ekleme
cursor.executemany('''
INSERT INTO Toprak_Bilgisi (Toprak_Turu, Urunler, Ozellikler)
VALUES (?, ?, ?)
''', veriler)

conn.commit()
conn.close()

print("Veritabanı oluşturuldu ve veriler eklendi.")
