MSFS 2024 – Livery 4K Converter 1.8 (Originalmaterialien und Batch-Verarbeitung)
==================================================

SPRACHAUSWAHL (NEU IN VERSION 1.5)
---------------------------------
- Oben rechts im Programmfenster kann zwischen „Deutsch“ und „English“ gewechselt werden.
- Die Auswahl gilt für Fenstertexte, Einstellungen, Dialoge, Statusmeldungen und neue Protokolleinträge.
- Die zuletzt gewählte Sprache wird automatisch für den nächsten Programmstart gespeichert.
- Bereits vorhandene Protokolleinträge behalten ihre ursprüngliche Sprache.

WAS NEU IN VERSION 1.8
----------------------
- Material- und Oberflächeneigenschaften werden grundsätzlich im Originalzustand belassen.
- Es gibt keine Auswahlmöglichkeit oder Regler zur Änderung von Mattheit, Glanz oder Metallanteil.
- COMP-/ORM-Texturen werden nicht gesondert bearbeitet. Liegen sie innerhalb der eingestellten Größenbegrenzung, werden sie unverändert kopiert.
- Überschreiten Texturen die eingestellte Maximalgröße, werden sie wie andere Texturen normal verkleinert und neu codiert. Dabei können durch Skalierung und Komprimierung technisch bedingte Pixelabweichungen entstehen; Materialkanäle werden jedoch nicht gezielt überschrieben.
- Diese Voreinstellung gilt gleichermaßen für Einzelkonvertierung und Batch-Verarbeitung.

HINWEIS ZUM ERHALT DER MATERIALIEN
----------------------------------
- Der Konverter nimmt keine gezielten Änderungen an Roughness, Metallic, Ambient Occlusion oder Alphakanälen vor.
- Texturen, die nicht verkleinert werden müssen, werden bytegenau in den Zielordner kopiert.
- Muss eine Textur verkleinert werden, kann die normale Bildskalierung bzw. Neu-Komprimierung Pixelwerte beeinflussen. Eine gezielte Materialanpassung findet nicht statt.
- Proprietär komprimierte MSFS-KTX2-Texturen (z. B. KTX2-Kennwert 65536) bleiben unverändert und werden im Protokoll als nicht direkt konvertierbar gemeldet.
- Die Quelldateien werden niemals verändert.

WAS NEU IN VERSION 1.7
----------------------
- Das Programmfenster passt seine Startgröße an die verfügbare Bildschirmfläche an.
- Ist der Bildschirm zu klein, erscheint rechts eine vertikale Scroll-Leiste. Dadurch bleiben auch die unteren Schaltflächen erreichbar.
- Nach Auswahl eines Quellordners wird der Zielordner automatisch auf denselben Pfad mit angehängtem _4K gesetzt.
- Ein nicht vorhandener Zielordner wird beim Start der Konvertierung automatisch erstellt.
- Neue Batch-Verarbeitung: Alle untergeordneten MSFS-Livery-Paketordner werden rekursiv erkannt und einzeln konvertiert.
- Für jedes Paket wird neben dem Quellordner ein Ausgabeordner mit angehängtem _4K erstellt.
- Bereits vorhandene _4K-Ausgabeordner werden vor dem Batch-Lauf vollständig geleert und neu aufgebaut.
- Ordner, deren Name auf _4K endet, werden niemals als Quell-Liveries behandelt.

WAS NEU IN VERSION 1.6
----------------------
- Die Programmoberfläche ist vollständig zweisprachig (Deutsch/Englisch).
- Nach erfolgreicher Änderung mindestens einer KTX2-Textur entfernt der Konverter alle kopierten .ktx2p-Dateien aus dem ZIELPAKET. Die Quelldateien bleiben erhalten.
- Die Sprachauswahl befindet sich oben rechts und wird beim nächsten Start beibehalten.
- Alle Funktionen aus Version 1.4 bleiben enthalten.
- Der Zielordner wird jetzt als vollständige Kopie des Quellordners aufgebaut.
- ALLE Dateien werden übernommen: manifest.json, layout.json, CFG/JSON/XML, Thumbnails,
  Dokumente, sonstige Dateien und alle Texturen.
- Texturen, die bereits 4K oder kleiner sind, bleiben unverändert.
- Nur zu große unterstützte Texturen werden verkleinert; COMP-/ORM-Materialkanäle werden nicht gezielt überschrieben.
- Die Ordnerstruktur und die Dateinamen bleiben erhalten.
- Optional kann MSFSLayoutGenerator.exe nach der Konvertierung automatisch ausgeführt
  werden, um layout.json und – sofern vorhanden – total_package_size in manifest.json
  zu aktualisieren.
- Die Quelldateien werden niemals verändert.

BATCH-VERARBEITUNG
------------------
- Den übergeordneten Ordner auswählen, der mehrere Livery-Pakete enthält.
- Die Option „Batch-Verarbeitung“ aktivieren und die Konvertierung starten.
- Das Programm sucht darunter nach MSFS-Paketwurzeln (mit SimObjects/Airplanes oder mit SimObjects plus manifest.json/layout.json).
- Jedes erkannte Paket wird in einen benachbarten Ordner mit dem Namen des Quellordners plus _4K kopiert und verarbeitet.
- Bereits vorhandene _4K-Zielordner werden nach einer Bestätigungsabfrage vollständig geleert. Dateien in den Quellpaketen bleiben unverändert.
- Vorhandene Ordner mit der Endung _4K werden bei der Suche übersprungen. Sie gelten ausschließlich als Ausgabeordner.
- Kategorien und beliebig tiefe übergeordnete Ordner bleiben erhalten; die einzelnen _4K-Ausgaben liegen jeweils neben ihrer Quell-Livery.

WAS DAS PROGRAMM MACHT
----------------------
- Durchsucht einen ausgewählten Lackierungs-/Paketordner einschließlich Unterordnern.
- Erstellt im Zielordner eine vollständige Dateikopie.
- Verkleinert nur Bilder, deren Breite ODER Höhe größer als die eingestellte Kantenlänge ist.
- Passt die Abmessungen proportional an; das Seitenverhältnis bleibt erhalten.
- Bei DDS werden Mipmaps neu erstellt.
- Bei unterstützten KTX2-Dateien wird die Textur auf Zielgröße skaliert, neu codiert und
  die Mipmap-Kette neu erzeugt.
- Native BC7-KTX2-Dateien (VK_FORMAT_BC7_UNORM_BLOCK und VK_FORMAT_BC7_SRGB_BLOCK)
  werden über DirectXTex/texconv verkleinert und wieder als KTX2 verpackt.
- Die BC7-Neukomprimierung kann DirectCompute auf einer NVIDIA-GPU verwenden; alternativ
  kann in der Programmoberfläche die CPU-Verarbeitung gewählt werden.
- Beim BC7-KTX2-Weg bleiben der KTX2-DFD- und der Key/Value-Metadatenblock erhalten,
  einschließlich ASOBO-Schlüsseln wie ASOBO_flags und ASOBOtexversion.

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

   Im Programm anschließend "ktx.exe" aus dem Ordner "bin" auswählen.

4. Pillow installieren:
   python -m pip install -r requirements.txt

5. MSFS Layout Generator (für fertige MSFS-Paketordner empfohlen):
   Release herunterladen:
   https://github.com/HughesMDflyer4/MSFSLayoutGenerator/releases/latest

   Die Datei "MSFSLayoutGenerator.exe" an einem festen Ort speichern und im Konverter
   bei "Layout-Tool" auswählen. Sie muss nicht in den Programmordner kopiert werden.

STARTEN
-------
Doppelklick auf "Starten.bat".

BEDIENUNG
---------
1. Als Quellordner den STAMMORDNER der vollständigen Lackierung/des Pakets auswählen.
   Das ist üblicherweise der Ordner, in dem manifest.json und layout.json liegen.
   Nicht nur den texture-Unterordner auswählen.
2. Einen separaten Zielordner auswählen. Der vorgeschlagene Name endet auf "_4K".
3. texconv.exe auswählen, falls sie nicht automatisch gefunden wurde.
4. ktx.exe auswählen, falls KTX2-Dateien vorhanden sind und das Programm sie nicht findet.
5. MSFSLayoutGenerator.exe im Feld "Layout-Tool" auswählen.
6. Maximale Kantenlänge 4096 belassen.
7. Für BC7 die GPU-Beschleunigung eingeschaltet lassen. Standardmäßig wird DirectCompute-
   Adapter 0 verwendet. Bei Hybrid-Notebooks ggf. Adapter 1 testen.
8. „Konvertierung starten“ anklicken. Material- und Oberflächeneigenschaften werden automatisch im Originalzustand belassen.

Der Konverter kopiert zuerst sämtliche Dateien in den Zielordner. Danach werden zu große
unterstützte Texturen verkleinert. Material- und Oberflächenkanäle werden nicht gezielt
verändert. Muss eine Textur neu skaliert oder komprimiert werden, können technisch bedingte
Pixelabweichungen entstehen. Schlägt eine Texturkonvertierung fehl, bleibt die zuvor kopierte
Originaldatei im Zielordner erhalten.

WICHTIG ZUM ZIELORDNER
----------------------
- Für ein sauberes Ergebnis möglichst einen neuen, leeren Zielordner verwenden.
- Wenn der Zielordner bereits Dateien enthält, werden Dateien mit gleichem relativen Pfad
  überschrieben. Zusätzliche Altdateien, die nicht mehr in der Quelle vorkommen, werden
  aus Sicherheitsgründen NICHT automatisch gelöscht.
- Der Quellordner bleibt immer unverändert.
- Ausnahme im ZIELORDNER: .ktx2p-Dateien werden nach erfolgreicher KTX2-Änderung entfernt,
  weil sie sonst veraltete Texturdaten bereitstellen könnten. Sie bleiben in der Quelle erhalten.

MSFS LAYOUT.JSON – BRAUCHE ICH MSFSLayoutGenerator.exe?
-------------------------------------------------------
Wenn der Quellordner eine layout.json enthält und Texturen verkleinert werden, sollte
layout.json nach der Konvertierung aktualisiert werden. Die Datei listet die Paketdateien
mit ihren Dateigrößen und Änderungszeiten auf. Nach einer Texturänderung stimmen diese
Angaben nicht mehr mit den Dateien überein.

Wenn "MSFSLayoutGenerator.exe" im Konverter ausgewählt ist, wird sie nach dem Kopieren
und Konvertieren automatisch mit der layout.json im Zielordner aufgerufen. Das Tool baut
die Dateiliste neu auf und aktualisiert in manifest.json auch total_package_size, sofern
diese Eigenschaft im Manifest vorhanden ist.

Wenn du das Layout-Tool nicht hinterlegst, werden alle Dateien trotzdem kopiert und die
Texturen trotzdem konvertiert. Der Konverter weist am Ende aber darauf hin, dass layout.json
noch aktualisiert werden muss. Du kannst dann die ZIEL-layout.json auf MSFSLayoutGenerator.exe
ziehen oder sie über das MSFS-SDK/den Package-Workflow neu erstellen.

Die MSFSLayoutGenerator.exe ist also nicht die Textur-Konvertierungsengine. Sie wird zum
Aktualisieren der Paketdateiliste benötigt (oder ein entsprechender SDK-/Layout-Workflow).
Für einen direkt verwendbaren Community-Paketordner empfehlen wir, sie einzubinden.

Beispiele für die Größenanpassung:
  8192 × 8192  ->  4096 × 4096
  8192 × 4096  ->  4096 × 2048
  8192 × 2048  ->  4096 × 1024
  4096 × 4096  ->  bleibt unverändert

KTX2-UNTERSTÜTZUNG UND GRENZEN
-----------------------------
Unterstützt werden standardkonforme 2D-KTX2-Texturen mit folgenden Formaten:
- BC7 UNORM und BC7 sRGB.
- UASTC / ETC1S (BasisLZ), sofern sie von der installierten KTX-Software gelesen werden.
- ASTC LDR-Texturen.
- 8-Bit RGB/RGBA UNORM- und sRGB-Texturen.

Die BC7-Neukomprimierung verwendet Microsoft DirectXTex/texconv. Mit aktivierter GPU-Option
übergibt das Programm den DirectCompute-Adapterindex über die texconv-Option -gpu.
Die Adapter-ID ist die DirectX-/DirectCompute-Gerätenummer und nicht zwingend identisch mit
der CUDA-Gerätenummer.

Einige MSFS-2024-Dateien sind keine normalen, öffentlich lesbaren KTX2-Dateien. Dateien
mit dem Supercompression-Kennwert 65536 werden erkannt, unverändert kopiert und für die
Konvertierung übersprungen. Für solche Dateien ist ggf. eine Extraktion über das MSFS
Livery Toolkit und anschließendes Neu-Bauen des Pakets mit dem MSFS-SDK notwendig:
https://github.com/theflaknine/MSFS-Livery-Toolkit/releases/latest

WICHTIG – KTX2P UND VRAM-REDUZIERUNG
------------------------------------
MSFS 2024 kann bei vorhandenen .ktx2p-Dateien weiterhin die darin gespeicherten alten
Texturdaten verwenden, obwohl einzelne .ktx2-Dateien verkleinert wurden. Microsoft
beschreibt dieses Verhalten in der SDK-Dokumentation und empfiehlt, KTX2P-Dateien nach
direkten Änderungen an KTX2 aus dem Paket zu entfernen.

Deshalb löscht Version 1.6 nach mindestens einer erfolgreich verkleinerten KTX2-Textur
automatisch alle .ktx2p-Dateien im ZIELORDNER. Die Originale im QUELLORDNER werden
niemals gelöscht. MSFS fällt anschließend auf die einzelnen KTX2-Dateien zurück.
Die layout.json wird danach – sofern MSFSLayoutGenerator.exe ausgewählt ist – neu
aufgebaut, damit auch die entfernten KTX2P-Dateien aus der Paketliste verschwinden.

Wenn keine KTX2-Textur erfolgreich verändert wurde, werden die KTX2P-Dateien nicht
entfernt. Verwende für jeden Lauf möglichst einen frischen, leeren Zielordner.

MSFS-HINWEISE
-------------
- Quellordner möglichst als vollständige Paketwurzel auswählen (manifest.json/layout.json).
- Den erzeugten Zielordner als separates Paket testen und das Original als Backup behalten.
- Bei Änderungen an bereits kompilierten/geschützten Add-ons kann ein Neu-Build mit dem
  MSFS-2024-SDK erforderlich sein.
- Achte darauf, dass das Add-on ausdrücklich mit MSFS 2024 kompatibel ist.

FEHLERBEHEBUNG
--------------
"texconv.exe fehlt":
  winget install Microsoft.DirectXTex.Texconv

"ktx.exe fehlt":
  Khronos KTX-Software installieren und die ktx.exe aus dem bin-Ordner auswählen.

"layout.json nicht aktualisiert":
  MSFSLayoutGenerator.exe herunterladen und in der Programmoberfläche bei "Layout-Tool"
  auswählen. Alternativ die layout.json aus dem ZIELORDNER auf die EXE ziehen.

"Pillow fehlt":
  python -m pip install -r requirements.txt

Lizenzhinweis:
Dieses Bedienprogramm verwendet Microsoft DirectXTex/texconv, Khronos KTX-Software und
optional MSFSLayoutGenerator als separate Werkzeuge. Es enthält diese Drittanbieter-Tools
nicht; deren jeweilige Lizenzbedingungen gelten separat.

GPU-HINWEIS
-----------
- Die GPU-Beschleunigung betrifft die BC7-Neukomprimierung in texconv.
- Aktiviert: texconv wird mit -gpu <Adapter-Index> aufgerufen.
- Deaktiviert: texconv wird mit -nogpu im CPU-Modus aufgerufen.
- Bei Fehlern zuerst Adapter 0/1 wechseln oder CPU-Modus aktivieren.

