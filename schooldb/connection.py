import mysql.connector
from datetime import datetime

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='++++++',
    database='schooldb'
)



def geburtsdatumÜberprüft(geburtsdatum):
    while True:
        try:    
            # GG.AA.YYYY formatını datetime objesine çevir
            date_obj = datetime.strptime(geburtsdatum, "%d.%m.%Y")
            # YYYY-MM-DD formatında string'e çevir
            return date_obj
        except ValueError:
            raise ValueError("Bitte geben Sie ein gültiges Datumsformat ein. Beispiel: 25.12.1995")
        
