// Headless smoke test. Usage: node tests/smoke.js path/to/session.jsonl
// Requires: npm i puppeteer-core, and Chrome (set CHROME=/path if not /usr/bin/google-chrome)
const p = require('puppeteer-core'), path = require('path');
(async () => {
  const jsonl = process.argv[2] || path.join(__dirname, '../src/base-session.jsonl');
  const b = await p.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox'] });
  const pg = await b.newPage(); await pg.setViewport({ width: 1400, height: 900 });
  const errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => m.type() == 'error' && errs.push(m.text()));
  await pg.goto('file://' + path.resolve(__dirname, '../dist/session-viewer.html'));
  await (await pg.$('#file')).uploadFile(path.resolve(jsonl));
  await new Promise(r => setTimeout(r, 4000));
  const fr = pg.frames().find(x => x !== pg.mainFrame());
  const r = await fr.evaluate(() => ({ messages: document.querySelectorAll('#messages > *').length, treeNodes: document.querySelectorAll('#tree-container .tree-node').length, title: document.querySelector('.header h1')?.textContent }));
  console.log(r, 'errors:', errs);
  await b.close();
  if (errs.length || !r.messages) process.exit(1);
})();
