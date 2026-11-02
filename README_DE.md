# MSFS 2024 – Livery 4K Converter

**[Deutsch](README_DE.md) | [English](README_EN.md)**

[![Lizenz: GPL-3.0-only](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

Ein Windows-Programm, das eine verkleinerte Kopie von Flugzeuglackierungen für Microsoft Flight Simulator 2024 erstellt. Der Quellordner bleibt unverändert; die Paketstruktur wird übernommen und unterstützte Texturen oberhalb einer einstellbaren Maximalgröße werden verkleinert.

> **Aktuellster bereitgestellter Quellstand:** v1.6 – KTX2P-Behandlung.  
> Die Git-Historie wird aus sieben ZIP-Snapshots rekonstruiert. Enthalten sind der ursprüngliche Konverter ohne KTX2-Unterstützung, ein späteres Archiv mit der Bezeichnung `v2` und erster KTX2-Verarbeitung sowie die anschließenden Stände v1.3 bis v1.6.

## Funktionen des neuesten bereitgestellten Stands

- Stapelverarbeitung eines vollständigen Lackierungs-/Paketordners einschließlich Unterordnern.
- Übernahme aller übrigen Dateien und Erhalt der Verzeichnisstruktur.
- Verkleinerung unterstützter Texturen oberhalb der eingestellten Maximalgröße (standardmäßig 4K).
- Verarbeitungspfade für DDS/KTX2 und BC7 gemäß der jeweils enthaltenen Programmversion.
- Auswahl einer DirectCompute-GPU für die BC7-Verarbeitung, sofern Werkzeug und Grafikkarte dies unterstützen.
- Optionaler Aufruf von MSFSLayoutGenerator zur Neuerstellung der `layout.json`.
- Deutsche und englische Programmoberfläche.
- Quelldateien bleiben unverändert; die Ausgabe erfolgt in einem separaten Zielordner.

## Voraussetzungen

- Windows 10/11.
- Python 3.10 oder neuer (die genaue Anforderung des ausgewählten Versionsstands beachten).
- Python-Abhängigkeit Pillow (`python -m pip install -r requirements.txt`).
- Microsoft DirectXTex `texconv.exe` für den DirectXTex-/DDS-/BC7-Workflow.
- Khronos KTX-Software `ktx.exe` für unterstützte KTX2-Operationen.
- MSFSLayoutGenerator ist optional. Nach Dateiänderungen muss `layout.json` jedoch neu erstellt werden. Das Programm kann das Werkzeug nach entsprechender Konfiguration aufrufen.

Externe Werkzeuge sind **nicht** in diesem Repository enthalten. Bitte von den offiziellen Projektseiten beziehen und deren Lizenzen beachten:

- [Microsoft DirectXTex](https://github.com/microsoft/DirectXTex)
- [KhronosGroup KTX-Software](https://github.com/KhronosGroup/KTX-Software)
- [MSFSLayoutGenerator](https://github.com/HughesMDflyer4/MSFSLayoutGenerator)

## Starten

1. Python installieren.
2. Die in `requirements.txt` aufgeführte Abhängigkeit installieren:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Benötigte externe Werkzeuge herunterladen und deren Pfade im Programm konfigurieren.
4. `Starten.bat` ausführen.

Weitere Informationen stehen in [README_DE.md](README_DE.md) und [README_EN.md](README_EN.md). Die ausführlichen Bedienungsanleitungen und BC7/KTX2-Hinweise liegen – sofern im neuesten Snapshot vorhanden – zusätzlich als `README_DE.txt`, `README_EN.txt`, `BC7_KTX2_HINWEIS.txt` und `BC7_KTX2_NOTE_EN.txt` bei.

## Wichtige Hinweise

- Immer einen separaten Zielordner verwenden. Niemals direkt im Quellpaket konvertieren.
- Nach Änderungen an Paketdateien muss `layout.json` vor dem Test in MSFS neu erstellt werden.
- Der Stand v1.6 entfernt laut bereitgestellter Implementierung kopierte `.ktx2p`-Dateien aus dem Zielpaket, nachdem mindestens eine KTX2-Textur erfolgreich konvertiert wurde. Der Quellordner bleibt unverändert. Das Ergebnis muss in MSFS geprüft werden.
- Eine geringere KTX2-Datenmenge ist nur ein Näherungswert und garantiert keine exakt entsprechende Reduktion der im Simulator gemessenen VRAM-Belegung. Laufzeit-Allokation, Streaming, LOD-Auswahl, Caching und weitere Flugzeugressourcen beeinflussen den VRAM. Für kontrollierte Vergleiche den SimObject Statistics Profiler im MSFS-DevMode verwenden.
- Vor dem Einsatz im Simulator eine Sicherung erstellen und das Ausgabepaket testen.

## Entwicklungshistorie

Siehe [CHANGELOG.md](CHANGELOG.md) und [HISTORY_RECONSTRUCTION.md](HISTORY_RECONSTRUCTION.md). Annotierte Git-Tags werden für v1.0 (ältester Snapshot, Versionsnummer abgeleitet), v1.3, v1.4, v1.5 und v1.6 erstellt. Das Archiv `MSFS4K_Converter_v2.zip` wird als nicht getaggter Zwischenstand mit erster KTX2-Verarbeitung aufgenommen, da sich seine genaue semantische Versionsnummer aus dem Archivinhalt nicht sicher bestimmen ließ. Weitere Zwischenversionen können fehlen.

Die ursprünglichen ZIP-Snapshots befinden sich im GitHub-Importpaket unter `history-archives/`, werden aber nicht in das erzeugte Git-Repository übernommen.

## Lizenz

Copyright (C) 2026 p0lfilt3r.

Dieses Projekt steht ausschließlich unter der **GNU General Public License Version 3.0 (GPL-3.0-only)**. Die Nutzung, Untersuchung, Veränderung und Weitergabe der Software sind unter den Bedingungen dieser Lizenz erlaubt. **Kommerzielle Nutzung ist ausdrücklich zulässig**; die GPL enthält keinen Ausschluss kommerzieller Nutzung. Bei der Weitergabe des Programms oder veränderter Versionen müssen die jeweils geltenden GPL-Anforderungen an Quellcode, Lizenzhinweise und Weitergabe eingehalten werden.

Der vollständige Lizenztext steht in [LICENSE](LICENSE). Diese Lizenz gilt für den Programmcode dieses Projekts; externe Werkzeuge unterliegen weiterhin ihren eigenen Lizenzen und Nutzungsbedingungen.
