# Übergabe: App prüfen und Design optimieren

## Links
- Repository: https://github.com/simeoncoester/Tech-Assistant-2.0 (Branch `main`)
- Live-App: https://simeoncoester.github.io/Tech-Assistant-2.0/
- Projektregeln und Architektur: `CLAUDE.md` im Repo-Root (zuerst komplett lesen)
- Die ganze App ist eine Datei: `index.html` (HTML + CSS + JS)

## Auftrag für die Nacht
1. **App prüfen:** alle Bereiche durchklicken (Drums, Gitarre/Bass, Live/Studio, Recording Chain inkl. Busse und Master Section, Mischpult, Foto-Recall, Hilfe, Einstellungen). Fehler, Konsolenfehler, Überlappungen, abgeschnittene Texte und ungewollte Scroll-/Wischfehler auf iPhone-Größe finden und beheben.
2. **Faceplates optimieren** (`FACEPLATES`, `fpSvg`, `prRealFace`, `prKnobSvg` in `index.html`):
   - Beschriftung darf sich nirgends mit Reglern, Skalen, LEDs, Metern oder dem Geräterand überschneiden.
   - Auf dem iPhone muss alles lesbar sein; große oder breite Geräte bekommen `pages` (Sektionen, Start mit „Alles“, Wischen).
   - Optik: metallisch, fotorealistisch, wie das Original, aber ohne Logos oder Fotos von Herstellern zu kopieren. Bedienelemente und Beschriftung müssen dem Original entsprechen und dürfen nicht abweichen (bei TL-Audio-VTC-Fadern gilt exakt die gedruckte Skala).
3. **Allgemeines Design:** Konsistenz, Abstände, Lesbarkeit im Hell-/Dunkelmodus, Bedienbarkeit mit dem Daumen.

## Regeln (aus CLAUDE.md, verbindlich)
- Pro Änderung `APP_VERSION` hochzählen, JS-Syntaxcheck, Tests, `CLAUDE.md` aktualisieren, deutsche Commit-Nachricht, Push auf `main`, danach den Workflow „pages build and deployment“ abwarten (bei Fehlschlag `pages-refresh.yml` erneut starten).
- Bestehende Funktionen nicht entfernen, gespeicherte Nutzerdaten (localStorage) müssen kompatibel bleiben (`normalize()`).
- Keine Hersteller- oder Händlerfotos in die App einbauen; Faceplates werden gezeichnet.

## Werkzeuge (Ordner `tools/`)
Voraussetzung: Node.js und Playwright mit Chromium. Lokalen Server im Repo-Root starten:

```bash
python3 -m http.server 8765
```

JS-Syntaxcheck:

```bash
sed -n '/<script>/,/<\/script>/p' index.html | sed '1d;$d' > /tmp/x.js && node --check /tmp/x.js
```

- `tools/fp-check.js`: prüft alle Faceplates auf Überschneidungen (Text/Regler/Skalen/LEDs/Meter/Rand). Optional mit Geräteliste: `node tools/fp-check.js "Manley VOXBOX,Bricasti M7"`. Ziel: „DEVICES WITH ISSUES: 0“. Gewollt sind nur die zwei LINK-Aufkleber bei Link Audio DYNX/SLQ.
- `tools/fp-legible.js`: misst auf iPhone-Größe die kleinste Schrift- und Reglergröße jedes Faceplates im Foto-Recall (beste Seite, ohne Zoom). Werte unter ca. 5 px sind nur mit Zoom lesbar; solche Geräte bei Gelegenheit in sinnvolle `pages` teilen.
- `tools/fp-sheet.js <ordner>`: rendert alle Faceplates als Übersichtsbilder.
- `tools/fp-shots.js <ordner> "Gerät A,Gerät B"`: öffnet Geräte im Foto-Recall und speichert Screenshots.
- `tools/tests/*.js`: Regressionstests. Im Ordner `tools/tests` ausführen, vorher `mkdir out`:
  - `test.js` (Gesamttest, erwartet „NO ISSUES“), `nullscan.js` („CLEAN“)
  - `swap.js` (Gerätewechsel tauscht Foto), `eye.js` (Auge Foto ↔ Faceplate), `choice.js` (Foto/Faceplate-Tasten, Amps), `fpsync.js`, `attach.js`
  - `pages.js`, `swipe.js`, `touch.js` (Seiten und Wischen auf iPhone-Größe), `zoom.js` (Lupe, Doppeltipp, Zwei-Finger-Zoom, automatische Seiten; erwartet „ZOOM OK“), `conc.js` (Doppelknöpfe getrennt drehbar, erwartet „CONC OK“), `tab.js` (untere Reiterleiste bleibt beim Scrollen unten, erwartet „TAB OK“), `fader.js`, `master.js` (Master Section), `disp.js` (Display-Texteingabe), `ampch.js` (Kanalnamen mehrerer Amps), `mob.js`

## Stand 14.11.2026 (1) – Übergabe an die nächste Sitzung
**Arbeitsweise, die sich bewährt hat**
- Vor jeder Arbeit `git fetch origin main && git merge --ff-only origin/main`; gearbeitet wird im Session-Branch, gepusht auf diesen Branch **und** auf `main` (vom Nutzer so gewünscht). Danach im GitHub-Workflow „pages build and deployment“ (Workflow-ID 393049086) den Erfolg abwarten.
- Commit-Nachrichten deutsch, mit den vom System vorgegebenen Trailern (Co-Authored-By/Claude-Session).
- Der Nutzer schreibt per Diktat und schickt Fotos/Screenshots; bei unleserlichen Details **nicht raten**, sondern nachfragen bzw. in der Antwort als „unsicher gelesen“ auflisten. Antworten kurz: was geändert wurde, wie man es bedient.
- Netz im Container eingeschränkt: Websuche geht, Abruf vieler Händler-/Handbuchseiten (vintageking.com, kmraudio.com, barryrudolph.com) nicht. PDFs, die der Nutzer hochlädt, mit `pdftotext`/`pdfimages` lesen.
- `tools/tests/undefined/*.png` werden von `test.js` überschrieben – vor dem Commit mit `git checkout -- tools/tests/undefined` zurücksetzen.

**Neu seit dem letzten Stand**
- Tablet und Handy (12.11. (9)/(10), 13.11. (1)): Mischpult füllt auf Tablets die Breite und zoomt (`fitConsole`, hört auf `resize`), Drum-Tuner quer größer, Handy quer mit flacher Reiterleiste und kompaktem Showmodus, Showmodus-Inhalt nie mehr oben abgeschnitten. Test: `tools/tests/tablet.js` (Viewport per `VP='[w,h,"dark"]'`, erwartet „TABLET OK“, läuft Minuten).
- Computer (13.11. (1)): Foto-Recall mit Trackpad-Pinch/Strg+Mausrad, Mausrad verschiebt, Tasten `+ - 0`, Pfeile = Seite; Escape schließt auch die Großansicht. Test: `tools/tests/desk.js` („DESK OK“).
- CAPI (13.11. (2)–(4)): 553F, VP25/26 (Gain-Kappe halb Orange/halb Blau über `q[7].c2`), VP28, VP312, LC4B (blau eloxierte Knöpfe über `q[7].bc`), LC25.
- Neve 8424 (13.11. (5)/(6)): Channel Strip und Master Section, nach dem Handbuch-PDF des Nutzers korrigiert. Generator `tools/neve8424-gen.py`.
- Neve 8058 (13.11. (7)): Channel Strip (Routing 32408 / Preamp & EQ 31102 / Aux & Monitor 32404 / Fader) und Master Section (Meter, Aux-Output-Matrix, Phase Meter, Oszillator, Rev Return to 4T, Aux/Group/4T Outputs, Solo Safe, Cue, Studio Loudspeaker, Input Selector, 4T Mixdown, Talkback, Monitor, Meters) – nur aus Fotos des Nutzers (PDF ohne Text) plus Websuche zu den 31102-Frequenzen. Generator `tools/neve8058-gen.py`.
- Generator-Muster für große Pulte: Python-Skript erzeugt die beiden JSON-Zeilen; in `index.html` die Zeilen, die mit `  "Neve 8058` beginnen, ersetzen (siehe Skriptkopf). Einträge stehen vor `'TL Audio VTC'`.

- Neve VR (13.11. (8)): Channel Strip (6 Spalten) und Master Section (11 Module) nach dem französischen VR-Skript des Nutzers (Text + Panel-Abbildungen mit Skalen). Generator `tools/nevevr-gen.py`. Unsicher: Skalen der Gate-/Kompressor-Knöpfe und der Mic-Gain-Rasterung (aus kleinen Abbildungen abgelesen), Large-/Small-Fader-Skala (10 … 0 … ∞ wie Abbildung S. 7), Lage der Cue-/Rev-Bedienelemente innerhalb der Module (Abbildungen nur schematisch).

- SSL 4000 E/G (13.11. (9)): Channel Strip (SL611G, 6 Spalten) und Master Section (SL651G + Centre Section, 17 Spalten in zwei Reihen, `build(..., PR)`) nach dem G-Handbuch des Nutzers (gescanntes PDF → Seiten als Bilder gelesen). Generator `tools/ssl4000eg-gen.py`.

- Audient ASP8024-HE (13.11. (10)): Channel Strip und Master Section nach der Broschüre; Master Section im Mischpult als Insert im Master-Zug; Übernahme-Dropdown nach Produktion gruppiert. Generator `tools/audient8024-gen.py`.

- Konsolen-Recherche (14.11. (1)): SSL ORIGIN, XL-Desk (je Kanal + Master) und AWS 948 (Kanal) aus offiziellen SSL-Handbüchern. Netzwerk-Umgebung „Tech-Assistant-2.0“ erlaubt solidstatelogic.com, manualslib, apiaudio, ams-neve, archive.org u. a. **Nächste Kandidaten:** SSL 9000 J/K (Handbuch nur auf manualmachine.com, dort 403), SSL Duality/AWS-Master, Neve Genesys/88RS, API Legacy/Vision, Harrison 32C, Trident 80B (nur Rack-Manual gefunden), Amek 9098, MCI JH-500. Knopffarben: ORIGIN nach Handbuchfoto, XL-Desk nach Handbuchtext, AWS nach Handbuchgrafik.

**Unsicher / beim Nutzer nachfragen (API 1608-II)**
- Doppelknöpfe der Aux-Sends: welches Label innen/außen liegt (angenommen: oberes Symbol = innerer Knopf).
- Kanal-VU und 944C-Automations-Taster angelegt; MUTE-GROUP-Taster am 840C grün (vom Nutzer bestätigt). 529C als eigenes Gerät (Kompressor), nicht in die 1608-Master-Section eingebaut (laut Handbuch nur 2448).
- Master-Section-Anordnung = Module nebeneinander wie im Handbuch, nicht nach Konsolenfoto; 529C-Kompressor gibt es nur bei der 2448 (nicht angelegt).
- Audient DLC jetzt angelegt (Stufenart Sonstiges); Beschriftung der Source/Dest-Felder „LINE I/P / S GRP“ bzw. „LINE O/P / S GRP“ vom Nutzer bestätigt. Audient ASP8024 Kanal: Beschriftung der beiden Shelf-Taster (AIR/100Hz von der HE übernommen) auf dem Foto nicht lesbar.

**Unsicher / beim Nutzer nachfragen (Audient ASP8024 / ASP8024-HE)**
- Kanalzug-Eingangssektion auf Wunsch logisch ergänzt (nicht nach Vorlage); Long Fader ohne Skala (Wunsch des Nutzers).
- Master Section nach Handbuch-Zeichnungen des Original-ASP8024; Anordnung der Sektionen untereinander (Konsolenfoto) nur ungefähr. Das Pult auf dem Foto hat mehr Aux-Master-Knöpfe als die Zeichnung (A, B, 1–4) – angelegt sind nur die gezeichneten. Wie viele Stereo-Eingänge (angelegt 4) und ob das HE dieselbe Master Section hat (angenommen, plus Kompressor und Heritage aus der Broschüre).
- Oszillator: zwei Taster ergeben 40 Hz/1k/10k/15k (Kombination laut Zeichnung).

**Unsicher / beim Nutzer nachfragen (SSL 4000 E/G)**
- Kappenfarben: Handbuch ist schwarz-weiß; EQ rot/grün/blau/schwarz (G), Gate grün, Kompressor schwarz, Filter grau sind typische Werte, nicht aus dem Handbuch.
- Skala des Hauptfaders (Control Room) im Handbuch nicht gedruckt → ohne Skala; Mic-Gain in 6-dB-Schritten nur als Punktring (+4…+70).
- Aux-Send-Knöpfe haben am Pult einen Druckschalter (gedrückt = an) – nicht als eigener Regler angelegt.
- E-Serie: statt x3/÷3 die BELL-Taster, kein Group-Trim-Pull, keine Stereo-VCAs und kein Local-Aux-Panel – die Faceplate zeigt den G-Stand.
- Lage der Elemente innerhalb der Spalten: aus den Einzelabbildungen, nicht 1:1 nach dem Gesamtplan.

**Unsicher / beim Nutzer nachfragen (Neve 8058)**
- 31102: Gain-Skala, Gain-Bereiche der EQ-Bänder und der kleine Taster neben HF („EQ-Taster“) sind nicht lesbar; Frequenzen (HF 10/12/16 kHz, Mid .35–7.2 kHz, LF 35–220 Hz, HPF 45–360 Hz, LPF 18–6 kHz) stammen aus der Websuche.
- 32404: Bedeutung der Taster unter Aux 1–4, der vier Monitor-Taster und der Mixdown-Taster; ob der hellblaue Knopf „Monitor Pan“ und der dunkelblaue „Mixdown Level“ ist.
- 32408: Skala des Direct-Level-Knopfs (nur Striche gezeichnet).
- Master: Beschriftung der Cue-Taster (rot/grün), Studio-LS-Taster („on“?), Talkback-Taster 5 („slate“/„mon“?), Oszillator-Schalter Mitte, zwei unbeschriftete Monitor-Wahltasten (nur gezeichnet), Fader-Skala (10 … 0 … ∞ nach Foto).

**Weiterhin offen (älter)**
- Auf echtem iPhone/iPad gegenprüfen: Zoom-Ebene im Foto-Recall, Reiterleiste `sticky`, PDF-Teilen/Speichern, Mischpult-Zoom auf dem Tablet, Showmodus im Handy-Querformat, Trackpad-Zoom in Safari.
- Lesbarkeit ohne Zoom (`fp-legible.js`): TL Audio VTC und Master Section, UA 6176/LA-610 MkII, VOXBOX, Shelford, SPL Transient Designer, DS201, Bricasti M7, Karacter 500.
- Behringer 369-KT: Langlöcher statt Eckschrauben; Neve 1084: HPF außen/LPF innen unbestätigt; DS201 LINK-Lage unbestätigt.

## Offene Punkte vom Nutzer
- Für Lexicon 480L/PCM96, EMT 140, Eventide H3000, Thermionic Culture Vulture und Elysia Karacter (19") fehlen noch Fotos – nicht raten, nicht anlegen.
- „SSL Kanal-Gate“: Rückfrage offen, ob es wie Link Audio DYNX angelegt werden soll.
- EMT 250: genaue Funktion der Hebel 2–4 unbestätigt (benannt nach Skalen).
