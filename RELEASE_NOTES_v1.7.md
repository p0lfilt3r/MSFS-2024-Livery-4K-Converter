# MSFS 2024 Livery 4K Converter v1.7

## Deutsch – Änderungen

**Korrektur gegenüber dem ersten v1.7-Testpaket:** Die Scroll-Leiste befindet sich jetzt rechts am Fensterrand.


- Das Programmfenster passt seine Startgröße an die verfügbare Bildschirmfläche an.
- Bei kleinen Bildschirmen erscheint rechts eine vertikale Scroll-Leiste, sodass alle Bedienelemente erreichbar bleiben.
- Nach der Quellordner-Auswahl wird automatisch ein benachbarter Zielpfad mit angehängtem `_4K` eingetragen.
- Nicht vorhandene Zielordner werden beim Start der Konvertierung automatisch erstellt.
- Neue Batch-Verarbeitung: Untergeordnete MSFS-Livery-Paketordner werden rekursiv erkannt und einzeln verarbeitet.
- Für jede Livery wird ein benachbarter Ausgabeordner mit angehängtem `_4K` erstellt.
- Vorhandene `_4K`-Ausgabeordner werden nach Bestätigung vollständig geleert und neu aufgebaut.
- Ordner, deren Name auf `_4K` endet, werden bei der Quell-Suche ignoriert und niemals als Liveries verarbeitet.

## English – Changes

**Correction to the first v1.7 test package:** The scrollbar is now positioned at the right edge of the window.


- The application window now sizes itself to the available display area.
- On smaller displays, a vertical scrollbar appears on the right so all controls remain accessible.
- Selecting a source folder automatically fills a sibling destination path with `_4K` appended.
- Missing destination folders are created automatically when conversion starts.
- New batch mode recursively discovers nested MSFS livery package folders and processes them individually.
- Each livery is written to a sibling output folder with `_4K` appended to its name.
- Existing `_4K` output folders are fully cleared and rebuilt after confirmation.
- Folders ending in `_4K` are ignored during source discovery and are never processed as liveries.

## Notes

The v1.7 GUI and batch file-handling logic passed automated tests in a simulated desktop environment. A Windows test with the user's installed DirectXTex/KTX tools and a real MSFS 2024 livery is still recommended before general distribution.
