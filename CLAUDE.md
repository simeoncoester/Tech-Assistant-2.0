# Tech Assistent – Projektnotiz für Claude

Web-App für Musiker, Backliner und Toningenieure (Drum-Tuning, Stimmgerät, Setlisten, Showmodus, Clicktrack, Recording Recall, Backups). Live unter **https://simeoncoester.github.io/Tech-Assistant-2.0/** (GitHub Pages, Branch `main`, Wurzelordner).

Der Projektinhaber kommuniziert auf **Deutsch**, oft per Diktat (Tippfehler wie „Moritz“ = „Notiz“ sinngemäß lesen). Er schickt häufig Screenshots vom iPhone/iPad. Antworten kurz zusammenfassen: was geändert wurde, wie es sich bedienen lässt.

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Die komplette App: HTML, CSS und JavaScript in **einer** Datei, keine Frameworks, kein Build-Schritt |
| `manifest.webmanifest` | PWA-Manifest (Home-Bildschirm-App) |
| `sw.js` | Service Worker: Seite network-first mit `cache: 'no-store'`, Rest cache-first; Cache-Name bei SW-Änderungen hochzählen |
| `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png` | App-Icons (Logo auf dunklem Grund) |

Externe Bibliotheken nur per CDN und erst bei Bedarf geladen: pdf.js, mammoth (Word), Tesseract.js 5.1.1 (Texterkennung), jsPDF 2.5.1, Google Fonts (Barlow, Barlow Condensed, Permanent Marker).

## Release-Ablauf (bei jeder Änderung)

1. `APP_VERSION` in `index.html` hochzählen, Format `'TT.MM.JJJJ (n)'` (steht unten auf der Startseite).
2. JavaScript-Syntax prüfen (Script-Block extrahieren, `node --check`).
3. Testen in den Viewports 375×667, 390×844, 768×1024, 1024×1366, 1440×900: kein seitliches Scrollen, keine Überlappungen in `.grid`/`.row`/`.chips`, keine Knöpfe außerhalb ihrer Karte.
4. Betroffene Abläufe im Browser durchklicken (Playwright), Konsole ohne Fehler.
5. Commit mit kurzer deutscher Beschreibung, Push auf `main`.

## Datenmodell

```
S.artists[] → { id, name, logoV, fontV, fontName, wordmarkV, wordmarkRatio, productions[] }
production  → { id, mode: 'live'|'studio', kind, name, date, venue, kit, notes,
                drums[], mics[], chain[], setlists[], tunings[], instruments[], instChains, backups[], hasPhoto }
setlist     → { id, mode, name, date, venue, songs[] }
song        → { id, title, key, bpm, sig, note, gt{tuning,capo}, bs{…}, sheet{…}, lyrics{…}, instNotes[] }
```

- `normalize()` migriert ältere Datenstände automatisch – neue Felder dort absichern.
- Speicher: `localStorage` (`drumtech-v1` = Hauptdaten, außerdem Route, Theme, Sprache, Onboarding, Eingangswahl, Installationshinweis).
- Große Dateien (PDF-Sheets, Backup-Dateien, Fotos) in IndexedDB über `FileStore`; Logos/Schriften über `saveAsset`/`getAsset`; Kit-Fotos über `savePhoto`/`getPhoto`.
- `touch()` speichert und markiert Änderungen; `render(true)` zeichnet neu.

## Navigation

- `route` + `nav(view, patch)`. Ablauf: Künstler → Live/Studio → Tour/Produktion → Instrument → Funktionen.
- Wischen links/rechts wechselt Bereiche, untere Leiste (`#tabbar`), Logo oben rechts = Startseite.
- Freier Tuner und Clicktrack sind ohne Künstler erreichbar (Symbole unten auf der Startseite); im freien Tuner Umschalter Drums/Bass/Gitarre in der Kopfzeile, Drums ist Standard.
- **Studio-Bereich ist für Tester gesperrt** („Under Construction“). Freischalten per URL `#studio-freigeben`, sperren per `#studio-sperren`.

## Wichtige Bereiche im Code

- **Tuner** (`Tuner`-Objekt): Drums (Lugs, Pitch, Resonanz), Bass/Gitarre (YIN). Mikrofon ohne Echo-/Rauschunterdrückung. Eingangswahl und Pegelanzeige (`inputPanel`, `Tuner.inputId`, `Tuner.inputLevel()`) für Gitarren-Adapter/Interfaces.
- **Tuning-Empfehlung** (`planTuning`, `showTuningSheet`): nur Toms (Snare/Bassdrum ausgeschlossen). Modi Setliste (Durchschnitt oder einzelner Song), Tonart, Intervalle. Schieberegler tief–hoch (`level`). Realistische Bereiche in `TOM_RANGE` (angelehnt an Tune-Bot; 16″ bis 60 Hz). Intervalle nach Kesselgröße: `ivBySize`.
- **Clicktrack** (`Click`): synthetisierte Sounds, Taktart, Betonungen, Unterteilung, Ausgabe akustisch/optisch. Optischer Impuls: alle Zählzeiten gleich hell, Betonung rot, BPM-Zahl blendet beim Laufen aus.
- **Setlisten**: Editor mit Titel/BPM/Takt, Notiz, Instrumente aus dem Speicher als Notiz-Karten (mit Kapo-Auswahl), Tonart, Stimmung/Kapo, „Chords und Lyrics“ (Chordsheet und Songtext: Datei oder Foto, auch handschriftlich, bearbeitbar, PDF-Export).
- **Import** (`importButton`, `importSetlistPhoto`, `parseSetlistMeta`, `parseSongs`, `parseSongLine`): erkennt Name, Datum, Ort und Spaltenköpfe. Fotos: in claude.ai liest Claude (`window.claude`), sonst Tesseract mit Vorverarbeitung (`ocrPrepare`: Median-Filter gegen Druckraster, Kontrast, Otsu-Schwelle; `cleanOcrLines`).
- **Großansicht** (`showStage`) und **Showmodus** (`showStageSong`): immer schwarz. Titel zentriert, Nummer links. Click-Pille mit Schloss (lange drücken = entsperren, temporäre Werte; Schließen = zurück auf gespeicherte Werte; bei Songs ohne Tempo wird beim Schließen gespeichert). Chords unten links, Lyrics unten rechts. Notizen mit „/“ getrennt = eigene Kacheln, Doppeltipp blendet aus.
- **Backups** (`viewBackups`): pro Produktion und Instrument, Gerätelisten `BACKUP_DEVICES` (Bass/Gitarre) und `BACKUP_DEVICES_DRUMS`.
- **Teilen** (`shareArtistDialog`, `shareProductionDialog`, `receivePayload`, `applyArtistPayload`, `applyPayload`): ganzer Künstler oder einzelne Tour, Künstlerprofil (Logo, Schrift, Schriftzug) reist immer mit. Link (`#import=` gzip) oder Datei (`.techassistent.json`).
- **Hilfe**: `START_SLIDES` (Startseite, 4 Folien), `HELP[view]` (Kontexthilfe), Grafiken in `ARTS`, Animationen in `DEMOS`, Folien über `SL(art, demo, title, text, steps, extra)`. Stichpunkte sind an Demo-Schritte gekoppelt; ohne Stichpunkte läuft die Demo automatisch.
- **PWA**: `registerSW` (nicht in claude.ai), Installationshinweis auf der Startseite (nur im Browser).

## Mehrsprachigkeit (Pflicht bei jeder Textänderung)

- Deutsch ist die Quellsprache im Code. Übersetzt wird zur Laufzeit ins Englische, Spanische und Französische.
- Wörterbuch `I18N` (eine Zeile JSON): `"Deutscher Text": ["English", "Español", "Français"]`. **Jeder neue sichtbare Text braucht einen Eintrag.**
- Dynamische Texte über Regex-Muster in der Musterliste (vor dem letzten Eintrag `/^(.+) – Tech Assistent$/` einfügen), Hilfsfunktion `L3(en, es, fr)`.
- Eigene Eingaben (Namen, Titel, Notizen) nicht übersetzen: Selektor `NO_I18N` bzw. Klasse `no-i18n`.
- Tonarten lokal (`keyLocal`), Zahlen und Datum im Landesformat.

## Design-Regeln

- Dunkles Design als Standard, helles Design über Klasse `ice`. Farben als CSS-Variablen.
- Glas-Optik: halbtransparente Flächen, feiner heller Rand, leichter Glanz oben; Pillen (`border-radius: 999px`) für Chips und kleine Knöpfe.
- Live = Rot, Studio = Blau. Kacheln ohne Erklärungstext (Erklärungen gehören in die Hilfe).
- Längliche Karten: ≡-Menü rechts (Umbenennen/Löschen mit Bestätigung), gedrückt halten = sortieren.
- Typografische Anführungszeichen im deutschen Text („…“), Apostroph ’.
- Layout-Sicherheit: Grid-Spalten mit `minmax(0,1fr)`, Felder `min-width: 0` (iOS-Datumsfelder!).

## Bekannte Grenzen

- `window.claude` (Bild-/Texterkennung durch Claude, Synchronisation) gibt es nur innerhalb von claude.ai. Auf GitHub immer eine Alternative auf dem Gerät anbieten.
- Daten liegen lokal pro Gerät; Safari und Home-Bildschirm-App speichern getrennt.
- Studio-Bereich ist noch in Arbeit.
