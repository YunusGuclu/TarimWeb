# tarım/management/commands/import_data.py

import pandas as pd
from django.core.management.base import BaseCommand
from tarım.models import GrainPrice  # GrainPrice modelini import ettik

class Command(BaseCommand):
    help = 'Excel dosyasından verileri alıp GrainPrice modeline aktarır'

    def handle(self, *args, **kwargs):
        excel_file = 'path_to_your_excel_file.xlsx'  # Excel dosyanızın yolu
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            grain_name = row['Tahıl Adı']  # Excel'deki tahıl adı sütunu
            price = row['2023']  # 2023 yılı fiyatı

            # GrainPrice modeline verileri ekliyoruz
            GrainPrice.objects.create(
                name=grain_name,
                price=price
            )

        self.stdout.write(self.style.SUCCESS('Veriler başarıyla aktarıldı!'))
