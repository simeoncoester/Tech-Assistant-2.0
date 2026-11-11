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
  - `pages.js`, `swipe.js`, `touch.js` (Seiten und Wischen auf iPhone-Größe), `zoom.js` (Lupe, Doppeltipp, Zwei-Finger-Zoom, automatische Seiten; erwartet „ZOOM OK“), `conc.js` (Doppelknöpfe getrennt drehbar, erwartet „CONC OK“), `fader.js`, `master.js` (Master Section), `disp.js` (Display-Texteingabe), `ampch.js` (Kanalnamen mehrerer Amps), `mob.js`

## Stand 11.11.2026 (7)
- Erledigt: Zoom im Foto-Recall, automatische Seiten für breite Geräte, Skalenstriche weichen Nachbarn aus, Rahmen-/Beschriftungsfehler (VTC Master Section, VOXBOX, SPL, DS201, EMT 250, TG2, GML 8200), größere Tippflächen im Mischpult.
- Zoom-Fehler vom iPhone behoben (34): Platte und Regler werden nur noch als eine Ebene skaliert; eine Zoom-Geste verstellt oder verschiebt keinen Regler mehr; verschobene Faceplate-Regler werden einmalig zurückgesetzt. Auf einem echten iPhone gegenprüfen (hier nur Chromium).
- Faceplate-Menü eingeschränkt (10.11. (1)): nur „Werte zurücksetzen“/„Von Stufe entfernen“, kein Umbenennen; „Regler setzen“ bleibt auch bei Faceplates; eigene Fotos behalten alle Optionen.
- Neu (10.11.): Klark Teknik 76-KT und Behringer 369-KT; Knöpfe plastischer (gedrehtes Metall, Rändel, Familien `urei`/`spun`/`nevecap`), Knöpfe auch in Vorschaubildern. Offen: übrige Knopf-Familien (`chicken`, `api`, `ssl`, `bakelite`, `marconi`) einzeln gegen Originalfotos nachschärfen; Behringer 369-KT hat im Foto Langlöcher statt Eckschrauben.
- Neu (11.11.): Doppelknöpfe mit Sweep, API 512c/550A und Neve 1073/1084/1073LB nach Fotos neu gebaut. Unbestätigt: beim Neve 1084 ist HPF dem äußeren Ring und LPF dem inneren Knopf zugeordnet; `Neve 1073` ist jetzt quer (wie Nutzerfoto) statt hochkant.
- Neu (11.11., Teil 2): Pultec EQP-1A/MEQ-5, Maag EQ4 und SSL E/G-Series EQ nach Fotos; SSL E- und G-Series EQ zusammengelegt (`fpRename`).
- Neu (11.11., Teil 3): Distressor EL8/EL8-X und API 2500 nach Fotos; LED-Anzeigen als antippbare Taster.
- Design-Durchsicht (11.11. (6)): Kippschalter bei 25 Geräten vergrößert, lange VU-Beschriftungen eingepasst, Einzelkorrekturen (siehe CLAUDE.md). ISA 428, ISA One und Avalon VT-737sp sind in (7) nach Nutzerfotos komplett beschriftet neu gebaut.
- Automatische Seiten teilen jetzt auch hohe Module (Oben/Unten) und kompakte Geräte nach Lesbarkeit.
- Noch offen (Lesbarkeit ohne Zoom, siehe `fp-legible.js`): Geräte mit eigenen `pages`, deren Bereiche auf dem iPhone noch zu klein sind – TL Audio VTC und Master Section, Universal Audio 6176 und LA-610 MkII, Manley VOXBOX, Shelford Channel, SPL Transient Designer, Drawmer DS201, Bricasti M7 – sowie Elysia Karacter 500 (sehr kleine Skalenzahlen). Dort hilft bisher der Zoom; feinere Seiten wären besser.
- Im Rahmen des Drawmer DS201 sitzt der LINK-Schalter knapp außerhalb von Kanal 2; Lage am Original unbestätigt (nicht geraten).

## Offene Punkte vom Nutzer
- Für Lexicon 480L/PCM96, EMT 140, Eventide H3000, Thermionic Culture Vulture und Elysia Karacter (19") fehlen noch Fotos – nicht raten, nicht anlegen.
- „SSL Kanal-Gate“: Rückfrage offen, ob es wie Link Audio DYNX angelegt werden soll.
- EMT 250: genaue Funktion der Hebel 2–4 unbestätigt (benannt nach Skalen).
