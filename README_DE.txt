MSFS 2024 – Livery 4K Converter
================================

WAS DAS PROGRAMM MACHT
----------------------
- Durchsucht einen ausgewählten Lackierungs-/Texturordner einschließlich Unterordnern.
- Verkleinert nur Bilder, deren Breite ODER Höhe größer als 4096 Pixel ist.
- Passt die Abmessungen proportional an; das Seitenverhältnis bleibt erhalten.
- Erhält Dateinamen und Unterordnerstruktur.
- Schreibt die neuen Texturen in einen separaten Zielordner.
- Ändert oder löscht niemals die Originaldateien.
- Bei DDS werden die Mipmaps neu erstellt. Das Eingabe-Pixel-Format wird beibehalten,
  da kein neues Ausgabeformat erzwungen wird.

VORAUSSETZUNGEN (WINDOWS 10/11)
-------------------------------
1. Python 3.9 oder neuer installieren, falls noch nicht vorhanden:
   https://www.python.org/downloads/windows/
   Bei der Installation "Add Python to PATH" aktivieren.

2. Microsoft DirectXTex / texconv installieren:
   PowerShell oder Eingabeaufforderung öffnen und ausführen:

   winget install Microsoft.DirectXTex.Texconv

   Offizielle Projekt-Dokumentation:
   https://github.com/microsoft/DirectXTex/wiki/texconv

3. Pillow installieren (für PNG/TGA/JPG/BMP/TIFF; für DDS allein nicht nötig):
   python -m pip install Pillow

STARTEN
-------
Doppelklick auf "Starten.bat".

BEDIENUNG
---------
1. Quellordner auswählen – beispielsweise den Ordner einer MSFS-Lackierung.
2. Zielordner auswählen. Vorschlag: ein neuer Ordner mit dem Zusatz "_4K".
3. Falls texconv.exe nicht automatisch gefunden wurde, die Datei auswählen.
4. Maximale Kantenlänge 4096 belassen.
5. "Konvertierung starten" anklicken.

Beispiele:
  8192 × 8192  ->  4096 × 4096
  8192 × 4096  ->  4096 × 2048
  8192 × 2048  ->  4096 × 1024
  4096 × 4096  ->  bleibt unverändert (wird übersprungen)

WICHTIGE HINWEISE
-----------------
- Vor dem Einbau in den Community-Ordner die konvertierte Lackierung testen.
- Den neuen Zielordner verwenden und die Original-Lackierung als Backup behalten.
- Die Bilddaten werden beim Herunterskalieren neu berechnet; das ist unvermeidbar.
- Unterstützte Dateiformate: DDS, PNG, TGA, JPG/JPEG, BMP, TIFF.
- DDS-Dateien mit komplexen Texturarrays/Cubemaps sind nicht der primäre Einsatzzweck;
  typische flache MSFS-Lackierungstexturen werden verarbeitet.

FEHLERBEHEBUNG
--------------
"texconv.exe fehlt":
  Installationsbefehl erneut ausführen und im Programm den Speicherort von texconv.exe
  über "Datei auswählen …" angeben.

"Pillow fehlt":
  python -m pip install Pillow

Lizenzhinweis:
  Dieses kleine Bedienprogramm verwendet Microsoft DirectXTex/texconv als separates
  Werkzeug. DirectXTex wird von Microsoft bereitgestellt; siehe Projektseite und Lizenz:
  https://github.com/microsoft/DirectXTex
