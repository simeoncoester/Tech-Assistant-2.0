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

## Stand 13.11.2026 (7) – Übergabe an die nächste Sitzung
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
