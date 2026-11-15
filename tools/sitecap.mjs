// Capture desktop + mobile screenshots of live sites (viewport only), dismissing cookie/newsletter overlays.
// usage: node sitecap.mjs <outDir> <slug=url> ...
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';

const [outDir, ...pairs] = process.argv.slice(2);
mkdirSync(outDir, { recursive: true });
const port = 9800 + Math.floor(Math.random() * 150);
const chrome = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', [
  '--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${outDir}/profile-${port}`,
  '--hide-scrollbars', '--no-first-run', '--disable-gpu', '--disable-blink-features=AutomationControlled', 'about:blank'
], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

for (let i = 0; i < 60; i++) { try { await fetch(`http://127.0.0.1:${port}/json/version`); break; } catch { await sleep(250); } }

const UA_D = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';
const UA_M = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1';

const CLEAN = `(function(){
  try{
    /* only press real accept/agree BUTTONS, never links (links navigate away) */
    var rx=/^(accept( all)?( cookies)?|allow all|agree|i agree|got it|alle akzeptieren|akzeptieren|zustimmen)$/i;
    document.querySelectorAll('button').forEach(function(b){var t=(b.textContent||'').trim();if(t.length<22&&rx.test(t)){try{b.click()}catch(e){}}});
    /* hide known consent managers + dialogs + big fixed overlays (keep the slim top header) */
    document.querySelectorAll('#usercentrics-root,#onetrust-banner-sdk,#CybotCookiebotDialog,#shopify-pc__banner,[role=dialog],[aria-modal=true],dialog,.klaviyo-form,.needsclick.kl-private-reset-css-Xuajs1').forEach(function(e){e.style.setProperty('display','none','important')});
    var bad=/cookie|consent|gdpr|popup|modal|klaviyo|attentive|privy|newsletter|subscribe|geo|country|overlay|age-gate|promo|chat|intercom|gorgias|tidio|accessib/i;
    document.querySelectorAll('body *').forEach(function(e){
      var s=getComputedStyle(e);
      if(s.position==='fixed'||s.position==='sticky'){
        var r=e.getBoundingClientRect();var id=(e.id||'')+' '+(typeof e.className==='string'?e.className:'');
        var big=(r.height>200&&r.width>260)||(r.height>120&&r.top>40&&r.width>300);
        if(bad.test(id)&&(r.height>30||r.width>150)||big&&!/header|nav|menu/i.test(id)&&e.tagName!=='HEADER'&&e.tagName!=='NAV')e.style.setProperty('display','none','important');
      }
    });
    document.documentElement.style.setProperty('overflow','auto','important');document.body&&document.body.style.setProperty('overflow','auto','important');
  }catch(e){}
})()`;

async function capture(slug, url, mobile) {
  const W = mobile ? 390 : 1440, H = mobile ? 844 : 900;
  const res = await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' });
  const t = await res.json();
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0; const pending = new Map(); let loaded = false;
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } if (m.method === 'Page.loadEventFired') loaded = true; };
  const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  try {
    await send('Page.enable'); await send('Runtime.enable');
    await send('Emulation.setUserAgentOverride', { userAgent: mobile ? UA_M : UA_D });
    await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: mobile ? 2 : 1, mobile });
    await send('Page.navigate', { url });
    for (let i = 0; i < 60 && !loaded; i++) await sleep(500);
    await sleep(8500);
    await send('Runtime.evaluate', { expression: CLEAN }); await sleep(1500);
    await send('Runtime.evaluate', { expression: CLEAN }); await sleep(700);
    await send('Runtime.evaluate', { expression: 'window.scrollTo(0,0)' }); await sleep(400);
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    writeFileSync(`${outDir}/${slug}-${mobile ? 'm' : 'd'}.png`, Buffer.from(shot.result.data, 'base64'));
    console.log('ok', slug, mobile ? 'mobile' : 'desktop');
  } catch (e) { console.log('FAIL', slug, mobile ? 'mobile' : 'desktop', e.message); }
  ws.close(); try { await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`); } catch {}
}

const jobs = [];
for (const p of pairs) { const [slug, ...u] = p.split('='); jobs.push([slug, u.join('='), false]); jobs.push([slug, u.join('='), true]); }
const queue = [...jobs];
await Promise.all(Array.from({ length: 4 }, async () => { while (queue.length) { const j = queue.shift(); await capture(...j); } }));
chrome.kill(); process.exit(0);
