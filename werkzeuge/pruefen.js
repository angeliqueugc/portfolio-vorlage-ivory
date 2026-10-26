// Seite prüfen und fertig machen, in einem Rutsch:
//   node werkzeuge/pruefen.js
// - Screenshots Handy + Laptop -> werkzeuge/ausgabe/ (zum Zeigen im Chat)
// - favicon.png, apple-touch-icon.png (aus favicon.svg) und bilder/vorschau-teilen.jpg (1200 × 630)
// - Liste aller übrigen Platzhalter, kaputten Links und zu großen Dateien
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const OUT = path.join(__dirname, 'ausgabe');
const url = f => 'file://' + path.join(SITE, f);

const PLATZHALTER = [
  [/class="ph[ "]/g, 'leere Bildfläche (class="ph")'],
  [/Dein Name|DEIN NAME/g, '„Dein Name“'],
  [/hallo@deinname\.de/g, 'Beispiel-E-Mail'],
  [/Marke (Eins|Zwei|Drei|Vier|Fünf|Sechs)|>Marke</g, 'Beispiel-Marke'],
  [/>0+[.,]?0* ?%?<|>000K</g, 'Beispiel-Zahl „00“'],
  [/href="https:\/\/(www\.)?(instagram|tiktok)\.com\/?"/g, 'Social-Link ohne Profil'],
  [/\[[A-ZÄÖÜ][^\]]{3,}\]/g, '[Platzhalter in eckigen Klammern]'],
  [/Hier steht/g, 'Beispieltext „Hier steht …“'],
];

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const probleme = [];
  const pages = fs.readdirSync(SITE).filter(f => f.endsWith('.html'));

  const browser = await chromium.launch();
  const fehler = [];
  const shot = async (opts, file, full) => {
    const p = await browser.newPage(opts);
    p.on('pageerror', e => fehler.push(e.message));
    await p.goto(url('index.html'));
    await p.evaluate(() => document.fonts.ready);
    const breite = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    if (breite) probleme.push(`${file}: Seite verrutscht seitlich`);
    await p.screenshot({ path: path.join(OUT, file), fullPage: full });
    return p;
  };
  await (await shot({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }, 'handy.png', true)).close();
  await (await shot({ viewport: { width: 1440, height: 900 } }, 'laptop.png', true)).close();

  // Vorschaubild für geteilte Links: oberer Teil der Startseite
  const og = await shot({ viewport: { width: 1200, height: 630 } }, 'og-test.png', false);
  await og.screenshot({ path: path.join(SITE, 'bilder', 'vorschau-teilen.jpg'), type: 'jpeg', quality: 82 });
  await og.close();
  fs.rmSync(path.join(OUT, 'og-test.png'));

  // Favicons aus favicon.svg
  const svg = fs.readFileSync(path.join(SITE, 'favicon.svg'), 'utf8');
  for (const [size, name] of [[64, 'favicon.png'], [180, 'apple-touch-icon.png']]) {
    const p = await browser.newPage({ viewport: { width: size, height: size } });
    await p.setContent(`<body style="margin:0;background:${size > 64 ? '#F6F2EA' : 'transparent'}">${svg.replace('<svg ', `<svg width="${size}" height="${size}" `)}</body>`);
    await p.screenshot({ path: path.join(SITE, name), omitBackground: size === 64 });
    await p.close();
  }
  await browser.close();

  // erst jetzt prüfen, damit die eben erzeugten Dateien mitzählen
  for (const f of pages) {
    const html = fs.readFileSync(path.join(SITE, f), 'utf8').replace(/<!--[\s\S]*?-->/g, '');
    for (const [re, name] of PLATZHALTER) {
      const n = (html.match(re) || []).length;
      if (n) probleme.push(`${f}: ${n}× ${name}`);
    }
    for (const m of html.matchAll(/(?:src|href|poster)="([^"#:?]+)"/g)) {
      if (!fs.existsSync(path.join(SITE, m[1]))) probleme.push(`${f}: Datei fehlt: ${m[1]}`);
    }
  }
  for (const dir of ['videos', 'bilder']) {
    const d = path.join(SITE, dir);
    if (!fs.existsSync(d)) continue;
    for (const f of fs.readdirSync(d)) {
      const mb = fs.statSync(path.join(d, f)).size / 1e6;
      if (mb > (dir === 'videos' ? 8 : 0.5)) probleme.push(`${dir}/${f} ist groß (${mb.toFixed(1)} MB)`);
    }
  }


  fehler.forEach(e => probleme.push('JavaScript-Fehler: ' + e));
  console.log('Screenshots: ' + path.join(OUT, 'handy.png') + ' und ' + path.join(OUT, 'laptop.png'));
  console.log('Erstellt: site/favicon.png, site/apple-touch-icon.png, site/bilder/vorschau-teilen.jpg');
  console.log(probleme.length ? '\nNOCH OFFEN:\n- ' + probleme.join('\n- ') : '\nAlles sauber: keine Platzhalter, keine kaputten Links.');
})();
