MSFS 2024 – Livery 4K Converter v1.8
Bedienungsanleitung (Deutsch)

Zweck
Das Programm erstellt eine separate, verkleinerte Kopie von MSFS-2024-Livery-Paketen. Quelldateien werden nicht verändert.

Voraussetzungen
- Windows 10/11
- Python 3.10 oder neuer
- Pillow (Installation: python -m pip install -r requirements.txt)
- Microsoft DirectXTex (texconv.exe) für unterstützte DDS-/BC7-Operationen
- Khronos KTX-Software (ktx.exe) für unterstützte KTX2-Operationen
- Optional: MSFSLayoutGenerator zum Neuerstellen der layout.json

Start
1. Benötigte Programme installieren und deren Pfade in den Einstellungen des Konverters angeben.
2. Starten.bat ausführen.
3. Sprache Deutsch oder Englisch auswählen.
4. Quellordner der Lackierung auswählen. Der Zielpfad wird automatisch mit dem Suffix _4K vorgeschlagen.
5. Bei Bedarf Batch-Verarbeitung aktivieren, um untergeordnete Livery-Pakete rekursiv zu verarbeiten.
6. Konvertierung starten. Fehlende Zielordner werden erstellt; vorhandene Batch-Zielordner werden nach Bestätigung neu aufgebaut.

Oberflächen- und Materialeigenschaften
Es gibt keine Auswahl zur Änderung von Mattheit, Glanz oder Metallanteil. Der Konverter überschreibt Materialkanäle wie Roughness, Metallic, Ambient Occlusion oder Alpha nicht gezielt. Texturen innerhalb der eingestellten Größenbegrenzung werden bytegenau kopiert. Größere Texturen durchlaufen die normale Verkleinerung und Neukodierung; dadurch können technisch bedingte Pixelabweichungen entstehen.

Wichtige Hinweise
- Niemals direkt im Quellpaket konvertieren; stets einen separaten Zielordner verwenden.
- Nach Änderungen am Paket muss layout.json neu erstellt werden, sofern das Flugzeugpaket dies erfordert.
- Das Ergebnis vor dem regulären Einsatz in MSFS 2024 testen.
- Externe Werkzeuge sind nicht im Paket enthalten und unterliegen ihren eigenen Lizenzen.
