# 🎓 Schulverwaltungsprojekt mit Python, Pandas & MySQL

## 📊 Projektbeschreibung

Dieses Projekt wurde entwickelt, um mit Python, Pandas und MySQL Operationen in der Datenbank einer Schule durchzuführen. Ziel ist es, den wöchentlichen Stundenplan automatisch zu erstellen, Daten zu aktualisieren, sie in die Datenbank zu speichern und den Stundenplan für jede Klasse als Excel-Dateien auszugeben.

## 📂 Hauptfunktionen

* Verwaltung von **Lehrern**, **Schülern**, **Fächern** und **Klassen**
* Automatische Generierung eines **wöchentlichen Stundenplans** unter Berücksichtigung von Lehrer-Verfügbarkeiten
* Speicherung der Stundenpläne in einer **MySQL-Datenbank**
* Export der Stundenpläne **klassenspezifisch als Excel-Dateien**

## 🔧 Technologien

* **Python 3**
* **MySQL** für Datenbankverwaltung
* **Pandas** zur effizienten Datenzuweisung und erleichterten Speicherung von Zeitplandaten

## 📚 Struktur

* `app.py`: Hauptmenü
* `connection.py`: Verbindungsaufbau zur MySQL-Datenbank
* `dbmanager_*.py`: Module zur Verwaltung von Klassen, Lehrern, Schülern, Stundenplänen
* `*.py`: Datenmodelle für Lehrer, Schüler, Klassen, Fächer etc.

## 📄 Beispiel: Excel-Stundenplan

Die Stundenpläne werden in einer übersichtlichen Tabellenform generiert:

* Zeilen = Unterrichtsstunden
* Spalten = Wochentage (Montag bis Freitag)
* Zellinhalte = Fach und Lehrername

## ✨ Ziel dieses Projekts

Ziel ist es, eine modulare und erweiterbare Schulverwaltungssoftware zu entwickeln, die eine effiziente Planung und Organisation des Schulbetriebs unterstützt. Das Projekt kann später durch Webschnittstellen, GUI-Module oder weitere Funktionen (z. B. Vertretungspläne) erweitert werden.


## 🚀 Starten des Projekts

1. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/RamazanOrsal/School_Database.git
   cd School_Database
   pip install pandas, mysql-connector-python

2.Führen Sie das Hauptskript aus:
  python app.py


---

Für weitere Details siehe Code und Kommentare in den jeweiligen Dateien.

> Projekt von [Ramazan Örsal](https://github.com/RamazanOrsal)
