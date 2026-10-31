MSFS 2024 – Livery 4K Converter 1.3 (NVIDIA-BC7)
=================================================

WAS DAS PROGRAMM MACHT
----------------------
- Durchsucht einen ausgewählten Lackierungs-/Texturordner einschließlich Unterordnern.
- Verkleinert nur Bilder, deren Breite ODER Höhe größer als die eingestellte Kantenlänge ist.
- Passt die Abmessungen proportional an; das Seitenverhältnis bleibt erhalten.
- Erhält Dateinamen und Unterordnerstruktur.
- Schreibt neue Texturen in einen separaten Zielordner.
- Ändert oder löscht niemals die Originaldateien.
- Bei DDS werden Mipmaps neu erstellt.
- Bei unterstützten KTX2-Dateien wird die Textur auf die Zielgröße skaliert, neu codiert
  und die Mipmap-Kette neu erzeugt.
- Native BC7-KTX2-Dateien (VK_FORMAT_BC7_UNORM_BLOCK und VK_FORMAT_BC7_SRGB_BLOCK)
  werden über DirectXTex/texconv verkleinert und wieder als KTX2 verpackt.
- Die BC7-Neukomprimierung kann DirectCompute auf einer NVIDIA-GPU verwenden; alternativ
  kann in der Programmoberfläche die CPU-Verarbeitung gewählt werden.
- Die vorhandenen KTX2-DFD- und Key/Value-Metadaten bleiben bei diesem BC7-Weg erhalten,
  einschließlich der ASOBO-Schlüssel wie ASOBO_flags und ASOBOtexversion.

VORAUSSETZUNGEN (WINDOWS 10/11)
-------------------------------
1. Python 3.9 oder neuer installieren, falls noch nicht vorhanden:
   https://www.python.org/downloads/windows/
   Bei der Installation "Add Python to PATH" aktivieren.

2. Microsoft DirectXTex / texconv installieren (für DDS, normale Bilddateien und BC7-KTX2):
   PowerShell oder Eingabeaufforderung öffnen und ausführen:

   winget install Microsoft.DirectXTex.Texconv

   Dokumentation:
   https://github.com/microsoft/DirectXTex/wiki/texconv

3. Khronos KTX-Software installieren (für KTX2-Dateien):
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
6. Für BC7 die GPU-Beschleunigung eingeschaltet lassen. Standardmäßig wird DirectCompute-Adapter 0 verwendet.
   Falls du mehrere Grafikkarten hast und Adapter 0 nicht die NVIDIA-Karte ist, teste Adapter 1.
   Wenn die GPU-Konvertierung fehlschlägt, Häkchen entfernen, um den CPU-Modus zu verwenden.
7. "Konvertierung starten" anklicken.

Beispiele:
  8192 × 8192  ->  4096 × 4096
  8192 × 4096  ->  4096 × 2048
  8192 × 2048  ->  4096 × 1024
  4096 × 4096  ->  bleibt unverändert (wird übersprungen)

KTX2-UNTERSTÜTZUNG UND GRENZEN
-----------------------------
Unterstützt werden standardkonforme 2D-KTX2-Texturen mit folgenden Formaten:
- BC7 UNORM und BC7 sRGB (VK_FORMAT_BC7_UNORM_BLOCK / VK_FORMAT_BC7_SRGB_BLOCK).
  Diese werden als BC7-Rohdaten in einen temporären DDS-Container übernommen, mit
  DirectXTex/texconv verkleinert und anschließend wieder als KTX2 verpackt. Der KTX2-DFD
  und der komplette Key/Value-Metadatenblock werden dabei aus dem Original übernommen.
  Das erhält auch ASOBO-Metadaten wie ASOBO_flags, ASOBO_opacities, ASOBO_transp und
  ASOBOtexversion.
- UASTC / ETC1S (BasisLZ), sofern sie von der installierten KTX-Software gelesen werden.
- ASTC LDR-Texturen.
- 8-Bit RGB/RGBA UNORM- und sRGB-Texturen.

Die BC7-Neukomprimierung verwendet Microsoft DirectXTex/texconv. Mit aktivierter GPU-Option
übergibt das Programm den DirectCompute-Adapterindex über die texconv-Option `-gpu`.
Microsoft dokumentiert diese GPU-Beschleunigung ausdrücklich für BC6H/BC7. Adapter 0 ist
der Standardadapter; auf Hybrid-Notebooks kann die NVIDIA-GPU unter Index 1 erreichbar sein.
Die Indexnummer ist der DirectX-/DirectCompute-Adapterindex und nicht zwingend identisch
mit der CUDA-Gerätenummer.

Das Bild wird beim Verkleinern neu gefiltert und BC7 erneut komprimiert; dadurch können
Dateigröße und Kompressionsqualität vom Original abweichen. Die Mipmap-Kette wird neu
aufgebaut. Der BC7-Weg verarbeitet normale 2D-Texturen; Arrays und Cubemaps werden nicht
automatisch verändert.

WICHTIG: Einige MSFS-2024-Dateien sind keine normalen, öffentlich lesbaren KTX2-Dateien.
Dateien mit dem Supercompression-Kennwert 65536 werden erkannt und übersprungen, statt
eine beschädigte Datei zu erzeugen. Die in manchen Lackierungen vorhandenen ASOBO_*-
Metadaten sind für sich genommen kein Fehler; beim BC7-Weg bleiben sie erhalten. Für genau diese MSFS-Sondervariante bietet das
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

"VK_FORMAT_BC7_UNORM_BLOCK wird nicht unterstützt":
  In Version 1.3 wird BC7 nicht mehr über PNG dekodiert. BC7-KTX2
  wird im Rohdatenmodus gelesen, über texconv als BC7-DDS skaliert und anschließend
  wieder als KTX2 verpackt. Stelle sicher, dass texconv.exe und ktx.exe ausgewählt sind.

"Pillow fehlt":
  python -m pip install -r requirements.txt

Lizenzhinweis:
Dieses Bedienprogramm verwendet Microsoft DirectXTex/texconv und Khronos KTX-Software
als separate Werkzeuge. Die jeweiligen Projekte und Lizenzbedingungen sind auf den
oben genannten Projektseiten aufgeführt.


GPU-HINWEIS
-----------
- Die GPU-Beschleunigung betrifft die BC7-Neukomprimierung in texconv.
- Aktiviert: texconv wird mit `-gpu <Adapter-Index>` aufgerufen.
- Deaktiviert: texconv wird mit `-nogpu` im CPU-Modus aufgerufen.
- Bei Fehlern zuerst Adapter 0/1 wechseln oder CPU-Modus aktivieren.
- Nicht jede Texturoperation läuft auf der GPU; das Filtern/Verkleinern kann weiterhin
  teilweise auf der CPU erfolgen.

Offizielle DirectXTex-Dokumentation zur GPU-Option:
https://github.com/microsoft/DirectXTex/wiki/texconv
