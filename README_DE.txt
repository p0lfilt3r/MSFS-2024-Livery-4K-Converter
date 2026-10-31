MSFS 2024 – Livery 4K Converter
================================

WAS DAS PROGRAMM MACHT
----------------------
- Durchsucht einen ausgewählten Lackierungs-/Texturordner einschließlich Unterordnern.
- Verkleinert nur Bilder, deren Breite ODER Höhe größer als die eingestellte Kantenlänge ist.
- Passt die Abmessungen proportional an; das Seitenverhältnis bleibt erhalten.
- Erhält Dateinamen und Unterordnerstruktur.
- Schreibt neue Texturen in einen separaten Zielordner.
- Ändert oder löscht niemals die Originaldateien.
- Bei DDS werden Mipmaps neu erstellt.
- Bei unterstützten KTX2-Dateien wird die Textur extrahiert, auf die Zielgröße skaliert,
  neu codiert und die Mipmap-Kette neu erzeugt.

VORAUSSETZUNGEN (WINDOWS 10/11)
-------------------------------
1. Python 3.9 oder neuer installieren, falls noch nicht vorhanden:
   https://www.python.org/downloads/windows/
   Bei der Installation "Add Python to PATH" aktivieren.

2. Microsoft DirectXTex / texconv installieren (für DDS und normale Bilddateien):
   PowerShell oder Eingabeaufforderung öffnen und ausführen:

   winget install Microsoft.DirectXTex.Texconv

   Dokumentation:
   https://github.com/microsoft/DirectXTex/wiki/texconv

3. Khronos KTX-Software installieren (nur für KTX2-Dateien):
   Windows-Version herunterladen und entpacken von:
   https://github.com/KhronosGroup/KTX-Software/releases

   Im Programm anschließend die Datei "ktx.exe" aus dem Ordner "bin" auswählen.
   Die KTX-Software stellt die Befehle zum Prüfen, Extrahieren und Neuerstellen
   standardkonformer KTX2-Dateien bereit.

4. Pillow für normale Bilddateien installieren:
   python -m pip install -r requirements.txt

STARTEN
-------
Doppelklick auf "Starten.bat".

BEDIENUNG
---------
1. Quellordner auswählen – beispielsweise den Ordner einer MSFS-Lackierung.
2. Zielordner auswählen. Vorschlag: ein neuer Ordner mit dem Zusatz "_4K".
3. Für DDS/Bilddateien texconv.exe auswählen, falls sie nicht automatisch gefunden wurde.
4. Für KTX2-Dateien ktx.exe auswählen, falls sie nicht automatisch gefunden wurde.
5. Maximale Kantenlänge 4096 belassen.
6. "Konvertierung starten" anklicken.

Beispiele:
  8192 × 8192  ->  4096 × 4096
  8192 × 4096  ->  4096 × 2048
  8192 × 2048  ->  4096 × 1024
  4096 × 4096  ->  bleibt unverändert (wird übersprungen)

KTX2-UNTERSTÜTZUNG UND GRENZEN
-----------------------------
Unterstützt werden standardkonforme 2D-KTX2-Texturen mit folgenden Formaten:
- UASTC / ETC1S (BasisLZ), sofern sie von der installierten KTX-Software gelesen werden.
- ASTC LDR-Texturen.
- 8-Bit RGB/RGBA UNORM- und sRGB-Texturen.

Die Software erstellt die KTX2-Datei neu und generiert die Mipmaps neu. Das Bild wird
neu codiert; dadurch können Dateigröße und Kompressionsqualität vom Original abweichen.
Es werden die KTX-Metadaten für Orientierung und Kanal-Swizzle übernommen, soweit vorhanden.
Andere herstellerspezifische Metadaten werden nicht garantiert übernommen.

WICHTIG: Einige MSFS-2024-Dateien sind keine normalen, öffentlich lesbaren KTX2-Dateien.
Dateien mit dem Supercompression-Kennwert 65536 werden erkannt und übersprungen, statt
eine beschädigte Datei zu erzeugen. Für genau diese MSFS-Sondervariante bietet das
separate Programm "MSFS Livery Toolkit" eine Extraktion in PNG an:
https://github.com/theflaknine/MSFS-Livery-Toolkit/releases/latest

Vorgehensweise für Kennwert 65536:
1. Die betreffende Textur mit "MSFS Livery Toolkit" über dessen Texture-Extraction-
   Funktion als PNG extrahieren.
2. Den Ordner mit diesen PNG-Dateien in diesem 4K Converter als Quelle auswählen.
3. PNGs auf 4096 Pixel verkleinern lassen.
4. Die verkleinerten PNGs im Livery-Projekt verwenden und das Paket anschließend über
   den MSFS-2024-SDK neu kompilieren.

Die Extraktion aus dieser Sonderkomprimierung ist in dieser kleinen Anwendung nicht
als automatischer Schritt eingebaut: Für das externe Toolkit ist keine unterstützte
Kommandozeilenschnittstelle zur automatischen Übergabe dokumentiert.

Gleiches gilt hier für nicht unterstützte Pixel-Formate, 3D-Texturen, Texture-Arrays,
Cubemaps und premultiplizierte Alpha-Texturen.

KTX2P-Dateien sind gepackte Streaming-Dateien und keine einzelnen Texturen; sie werden
nicht verarbeitet.

WICHTIGE MSFS-HINWEISE
---------------------
- Vor dem Einbau in den Community-Ordner die konvertierte Lackierung testen.
- Den neuen Zielordner verwenden und die Original-Lackierung als Backup behalten.
- Bei bereits gebauten MSFS-Paketen ist das direkte Ändern der kompilierten Texturen
  nicht der empfohlene SDK-Arbeitsablauf. Wenn möglich, die Quelldateien verkleinern
  und das Paket anschließend mit dem MSFS-2024-SDK neu bauen.
- Marketplace- bzw. anderweitig proprietär geschützte Inhalte können nicht mit
  allgemeinen KTX-Werkzeugen bearbeitet werden.

FEHLERBEHEBUNG
--------------
"texconv.exe fehlt":
  winget install Microsoft.DirectXTex.Texconv
  Danach texconv.exe im Programm auswählen.

"ktx.exe fehlt":
  Khronos KTX-Software über den oben genannten Release-Link herunterladen,
  entpacken und die ktx.exe aus dem bin-Ordner auswählen.

"Pillow fehlt":
  python -m pip install -r requirements.txt

Lizenzhinweis:
Dieses Bedienprogramm verwendet Microsoft DirectXTex/texconv und Khronos KTX-Software
als separate Werkzeuge. Die jeweiligen Projekte und Lizenzbedingungen sind auf den
oben genannten Projektseiten aufgeführt.
