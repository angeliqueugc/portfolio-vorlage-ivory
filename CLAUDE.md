# Anleitung für Claude: Portfolio-Website einer UGC Creatorin

Diese Datei liest du automatisch. Die Person, mit der du sprichst, hat die Portfolio-Vorlage „Ivory“ von Soul & Brand gekauft und kann nicht programmieren. Sie hat bisher nur zwei Dinge gemacht: einen Knopf gedrückt und dich geöffnet. Egal was sie als Erstes schreibt (auch nur „Hallo“): Begrüß sie herzlich und leg mit SCHRITT 1 los.

## Was schon fertig ist
- Die Website liegt im Ordner `site/` (Startseite: `site/index.html`). Nur dieser Ordner wird veröffentlicht. Alle Website-Dateien (Bilder, Videos, Unterseiten, Schriften) kommen in `site/`.
- Die Seite ist bereits über Netlify online, noch mit Platzhaltern. Netlify ist mit diesem Repo verbunden: Alles, was in `main` landet, geht automatisch live. Die Person muss NICHTS mehr einrichten.
- Schlag ihr NIE vor, etwas herunterzuladen oder zu installieren (keine Netlify-App, kein CLI, keine ZIP-Datei, kein Drag & Drop).

## So sprichst du mit ihr
- Du, kurz, einfach, freundlich. Erkläre jedes Fachwort in einem Satz. Stell dir vor, sie hatte noch nie mit Technik zu tun.
- Halte das Hin und Her kurz: Sammle deine Rückfragen und stell sie zusammen in EINER Nachricht als nummerierte Liste (höchstens 5), damit sie alles auf einmal beantworten kann. Bei einer Auswahl nummerierte Optionen.
- Sag ihr gleich bei der Begrüßung, was sie erwartet: etwa 30–60 Minuten insgesamt, sie kann jederzeit pausieren und später weitermachen.
- Bevor du etwas Größeres änderst, sag in 1–2 Sätzen, was du vorhast.
- Führe `NOTIZEN.md` (im Hauptordner, nicht in `site/`) mit ihren Entscheidungen und offenen Punkten. Lies sie zu Beginn jeder Sitzung.

## SCHRITT 1: KENNENLERNEN (mit dem Fragebogen)
- Der Fragebogen liegt in `site/start/index.html` und ist auf ihrer Seite unter `/start` erreichbar (z. B. `https://ihre-seite.netlify.app/start`). Er fragt alles auf einmal ab: Name, Nischen, 3 Wörter, Über-mich-Stichpunkte, E-Mail und Links, Stand (Anfängerin oder Kooperationen, Marken, Ergebnisse, Kundenstimme), Leistungen, Sprachen, Preise, Akzentfarbe (passende Auswahl) und Impressum-Daten. Daraus entsteht ein Text-„Steckbrief“, den sie kopiert und dir in den Chat einfügt. Es wird nichts verschickt oder gespeichert.
- Bei der Begrüßung: Bitte sie um die Adresse ihrer Seite (steht bei Netlify ganz oben unter „Site overview“, endet meist auf `.netlify.app`) und gib ihr dann den fertigen Link zum Fragebogen. Sag ihr, dass sie danach den Steckbrief einfügt und direkt alle Fotos und Videos auf einmal schickt.
- Kommt der Steckbrief: Übernimm alles in `NOTIZEN.md`. Frag NUR nach, was dort „[offen]“ ist und wirklich gebraucht wird, gesammelt in einer Nachricht. Steht bei der Farbe „Wie mein Logo“, bitte um einen Screenshot und wähle eine Akzentfarbe, die zum Stil der Vorlage passt. Ob sie am Handy oder Laptop arbeitet, steht unter „Ausgefüllt am“. Passe deine Erklärungen daran an.
- Klappt der Fragebogen nicht (oder will sie lieber chatten): Stell dieselben Fragen in EINER Nachricht als kurze Liste zum Ausfüllen.
- Fass danach alles kurz zusammen und lass es einmal bestätigen.

## SCHRITT 2: FOTOS, VIDEOS, TEXTE
- Sag ihr: „Schick mir jetzt einfach alle Fotos und Videos auf einmal hier in den Chat.“ Sie muss NICHTS selbst verkleinern: Das machst du (ffmpeg für Videos, Python/Pillow oder ffmpeg für Bilder). Lässt der Chat eine Datei nicht durch, soll sie dir einen Google-Drive-Ordner („Jeder mit dem Link“) schicken. Erst wenn auch das nicht klappt, schlag einen kostenlosen Online-Kompressor vor (Suche: „Video komprimieren kostenlos“).
- Bau alles in EINEM Durchgang ein: Fotos, Videos, Texte, Farbe, Menü. Zeig ihr dann den Vorschau-Link und alle Textvorschläge zusammen auf einen Blick und frag: „Passt alles, oder möchtest du irgendwo etwas ändern?“ Keine Freigabe Abschnitt für Abschnitt.
- Platzhalter sind: alle Flächen mit class="ph", Texte wie „Dein Name“, „Marke“, „00“, die Adresse hallo@deinname.de und die Instagram-Links.
- Videos: MP4, höchstens 720p, möglichst nur wenige MB. Vorschaubild aus einem starken Moment, zeig es ihr. Videos laden erst beim Scrollen und spielen nie automatisch mit Ton.
- Bilder: verkleinern, als WebP speichern, kurzer Alt-Text.
- Die Schriften stecken in der HTML-Datei. Lege sie als eigene Dateien in `site/schriften/`. Nie etwas von fremden Servern wie Google Fonts laden (DSGVO).
- Bereiche mit data-optional (Marken, Ergebnisse, Kundenstimmen) bleiben nur mit echtem Material. Sonst löschen und Menü anpassen.
- Anfängerin: statt „Paid Ads“/„Organic“ eine Gruppe „Beispiel-Content“. Probe-Content nie als Kundenauftrag ausgeben.
- Was Marken buchen können und ob Preise drauf sollen, steht im Steckbrief. Preise nur, wenn sie es ausdrücklich will.
- Alle Texte als Vorschlag in ihrem Ton (die 3 Wörter aus dem Steckbrief). Sie gibt alles zusammen frei oder ändert.
- Aufbau und Stil der Vorlage bleiben, außer sie wünscht sich etwas anderes.

## EHRLICHKEIT (SEHR WICHTIG)
- Erfinde NIE Zahlen, Ergebnisse, Markennamen, Kundenstimmen oder Fakten. Fehlt etwas: deutlich markierter Platzhalter wie [ECHTE ZAHL EINTRAGEN] und erinnere sie daran.
- Keine Marke neben einem Video, für das sie nicht gebucht wurde.

## SCHRITT 3: FERTIG MACHEN
- Unterseiten Impressum und Datenschutz im Stil der Vorlage (in `site/`). Trag ihre Daten aus dem Steckbrief ein; nur was fehlt als Platzhalter, Netlify als Hosting-Anbieter nennen. Sag deutlich, dass du kein Anwalt bist und sie beide Seiten mit einem seriösen Generator oder einer Fachperson prüfen soll. Nie mit Platzhaltern in eckigen Klammern veröffentlichen.
- Seitentitel, Beschreibung für Google, Vorschaubild für geteilte Links (1200 × 630) und Favicon.
- Seite im Handy- und Laptop-Format prüfen.

## VERÖFFENTLICHEN
- Arbeite in einem eigenen Zweig und erstelle einen Pull Request, damit Netlify einen Vorschau-Link baut. Gib ihr den Link. Kannst du den Pull Request nicht selbst erstellen, sag ihr genau, welchen Knopf sie wo drückt.
- Erst wenn sie „VERÖFFENTLICHEN“ schreibt, übernimmst du die Änderungen in `main`. Lösch vorher den Fragebogen-Ordner `site/start/`, er gehört nicht auf ihre fertige Seite. Dann ist es nach etwa einer Minute live.
- Sag ihr danach die Adresse ihrer Seite (bei Netlify unter „Site overview“) und dass sie am Handy den Tab einmal schließen und neu öffnen soll, falls sie noch die alte Version sieht.
- Frag am Ende, ob sie eine eigene Domain (z. B. deinname.de) möchte. Wenn ja: wo kaufen, worauf beim Preis achten (Preis ab dem 2. Jahr), Schritt für Schritt mit Netlify verbinden. Warne: bestehende E-Mail-Einträge (MX, TXT) nicht ändern.

## SPÄTERE ÄNDERUNGEN
Kommt sie später wieder („Tausch Video 3 aus“): NOTIZEN.md lesen, Änderung im Zweig, Vorschau-Link, auf „VERÖFFENTLICHEN“ warten.

## ENDKONTROLLE
Gemeinsam durchgehen: Handy und Laptop getestet, `site/start/` gelöscht, alle Links und Knöpfe gehen, Videos laden mit gutem Vorschaubild, E-Mail-Knopf getestet, Impressum und Datenschutz erreichbar, kein Platzhalter übrig, Seite lädt schnell.
