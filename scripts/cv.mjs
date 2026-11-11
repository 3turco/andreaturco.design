// Genera public/cv-andrea-turco.pdf da cv/cv.html con Chrome senza interfaccia.
// Chrome produce un PDF taggato: struttura dei titoli, lingua, testo alternativo,
// elementi con aria-hidden. Poi cv-pdfua.py lo rifinisce per PDF/UA. Uso: npm run cv
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const chrome = [
  process.env.CHROME_PATH,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
].find((p) => p && existsSync(p));

if (!chrome) {
  console.error('Chrome non trovato. Indica il percorso con CHROME_PATH.');
  process.exit(1);
}

const sorgente = pathToFileURL(fileURLToPath(new URL('../cv/cv.html', import.meta.url))).href;
const destinazione = fileURLToPath(new URL('../public/cv-andrea-turco.pdf', import.meta.url));

execFileSync(chrome, [
  '--headless',
  '--disable-gpu',
  '--no-pdf-header-footer',
  '--export-tagged-pdf',
  '--generate-pdf-document-outline',
  `--print-to-pdf=${destinazione}`,
  sorgente,
], { stdio: 'inherit' });

// Rifinitura PDF/UA: artefatti, LBody, metadati XMP. PYTHON permette un ambiente con pikepdf.
execFileSync(process.env.PYTHON || 'python3', [
  fileURLToPath(new URL('./cv-pdfua.py', import.meta.url)),
  destinazione,
], { stdio: 'inherit' });

console.log(`CV scritto in ${destinazione}`);
