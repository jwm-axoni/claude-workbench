// Renders each section of docs/index.html to docs/assets/*.png for the README.
// Usage: node docs/render-assets.js   (needs Node and Playwright with Chromium)
const { chromium } = require('playwright');
const out = require('path').join(__dirname, 'assets') + '/';
const shots = [
  ['tab-start','box-h','workbench-whats-in-the-box'],
  ['tab-setup','setup-h','workbench-setup'],
  ['tab-setup','src-h','workbench-role-packs'],
  ['tab-folder','folder-h','workbench-folder'],
  ['tab-folder','ledger-h','workbench-read-the-page'],
  ['tab-routines','chain-h','workbench-daily-chain'],
  ['tab-routines','dream-h','workbench-nightly-dream'],
  ['tab-routines','week-h','workbench-week'],
  ['tab-learning','deliver-h','workbench-delivery'],
  ['tab-learning','learn-h','workbench-learning'],
  ['tab-learning','project-h','workbench-one-project'],
  ['tab-skills','skills-h','workbench-skills'],
  ['tab-memory','mem-h','workbench-memory'],
  ['tab-memory','mig-h','workbench-moving-over'],
];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1180,height:1000}, deviceScaleFactor:2, reducedMotion:'reduce' });
  for (const [tab, h, name] of shots) {
    await p.goto('file://' + require('path').join(__dirname, 'index.html') + '#'+tab); await p.waitForTimeout(900);
    const sec = p.locator(`#${h}`).locator('xpath=ancestor::section[1]');
    await sec.scrollIntoViewIfNeeded(); await p.waitForTimeout(700);
    const r = await sec.evaluate(el=>{const b=el.getBoundingClientRect();return {x:b.x+scrollX,y:b.y+scrollY,w:b.width,h:b.height};});
    const pad=36;
    await p.screenshot({ path: out + name + '.png', fullPage:true, clip:{x:Math.max(0,r.x-pad),y:Math.max(0,r.y-pad),width:r.w+pad*2,height:r.h+pad*2} });
  }
  // header banner and plugin icon, each from its own HTML source in docs/assets/
  const h = await b.newPage({ viewport:{width:1280,height:470}, deviceScaleFactor:2 });
  await h.goto('file://' + require('path').join(__dirname, 'assets', 'workbench-header.html')); await h.waitForTimeout(400);
  await h.locator('#header').screenshot({ path: out + 'workbench-header.png' });
  const i = await b.newPage({ viewport:{width:512,height:512}, deviceScaleFactor:1 });
  await i.goto('file://' + require('path').join(__dirname, 'assets', 'workbench-icon.html')); await i.waitForTimeout(300);
  await i.locator('#icon').screenshot({ path: require('path').join(__dirname, '..', '.claude-plugin', 'icon.png') });
  // 1280x640 social preview for GitHub (Settings > Social preview)
  const g = await b.newPage({ viewport:{width:1280,height:640}, deviceScaleFactor:1 });
  await g.goto('file://' + require('path').join(__dirname, 'assets', 'workbench-header.html'));
  await g.addStyleTag({content:'html,body{height:640px;display:grid;place-items:center;background:#232323} svg rect[filter]{display:none}'});
  await g.waitForTimeout(300);
  await g.screenshot({ path: out + 'workbench-social.png' });
  await b.close();
})();
