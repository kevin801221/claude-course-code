#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { accessSync, constants, existsSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, writeFileSync, copyFileSync } from 'node:fs';
import { delimiter, dirname, join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { basename } from 'node:path';
import { extractLayout } from './svg-layout.mjs';

const usage = `Render a Mermaid flowchart and inspect its geometry.
Usage: node render.mjs input.mmd --out preview --width 760
Options:
  --out PREFIX                  Output prefix (default: input without .mmd)
  --width CSS_PX                Display container width (default: 760)
  --mmdc PATH                   Existing Mermaid CLI executable
  --puppeteer-config FILE       Existing Puppeteer JSON launch settings
  --formats png,svg,pdf         Formats to retain (default: png,svg)
  --layout FILE                 Write native SVG geometry for editable PPTX
Produces selected PREFIX.svg, PREFIX.png (2x pixels), PREFIX.pdf, and PREFIX.metrics.json.
PDF uses native SVG size on one vector page (maximum 200 inches per side).
Requires Node.js and an existing mmdc installation with Puppeteer.
This tool does not certify aesthetics or replace visual inspection.`;

function findExecutable(name) {
  if (name.includes('/') || name.includes('\\')) return realpathSync(resolve(name));
  for (const dir of (process.env.PATH || '').split(delimiter)) {
    const candidate = join(dir, name);
    try { accessSync(candidate, constants.X_OK); return realpathSync(candidate); } catch {}
  }
  throw new Error(`Cannot find ${name}. Use an existing Mermaid CLI via --mmdc; no packages were installed.`);
}

function findPuppeteer(cli) {
  const candidates = [cli, join(process.cwd(), 'package.json')];
  for (const path of candidates) {
    try { return createRequire(path)('puppeteer'); } catch {}
  }
  throw new Error('Cannot resolve Puppeteer from the existing Mermaid CLI or current project. Use a supported existing installation or render in the target host.');
}

function existingBrowser(puppeteer) {
  try { if (existsSync(puppeteer.executablePath())) return puppeteer.executablePath(); } catch {}
  if (process.platform === 'darwin') {
    const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
    if (existsSync(chrome)) return chrome;
  }
  for (const name of ['chromium', 'chromium-browser', 'google-chrome']) {
    try { return findExecutable(name); } catch {}
  }
  throw new Error('No existing Chrome/Chromium found. Pass --puppeteer-config with an existing executablePath, or render in the target host. No browser was installed.');
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) { console.log(usage); return; }
  if (!args.length || args[0].startsWith('-')) throw new Error(usage);
  const input = resolve(args.shift());
  const opts = { out: input.replace(/\.mmd$/i, '') + '.preview', width: '760', mmdc: 'mmdc', formats: 'png,svg' };
  const allowed = new Set(['out', 'width', 'mmdc', 'puppeteer-config','formats','layout']);
  while (args.length) {
    const flag = args.shift();
    if (!flag.startsWith('--') || !allowed.has(flag.slice(2)) || !args.length) throw new Error(`Invalid option: ${flag}\n${usage}`);
    opts[flag.slice(2)] = args.shift();
  }
  const width = Number(opts.width);
  const formats=new Set(opts.formats.split(','));
  if(!formats.size || [...formats].some(f=>!['png','svg','pdf'].includes(f))) throw new Error('--formats supports png,svg,pdf only. Use export.mjs for PPTX.');
  if (!Number.isFinite(width) || width < 200 || width > 5000) throw new Error('--width must be between 200 and 5000 CSS pixels.');
  if (!existsSync(input)) throw new Error(`Input not found: ${input}`);
  const cli = findExecutable(opts.mmdc);
  const puppeteer = findPuppeteer(cli);
  const prefix = resolve(opts.out);
  if (/\.pdf$/i.test(prefix)) throw new Error('--out is a prefix without an extension; use --formats pdf.');
  if (input === prefix + '.pdf' || input === prefix + '.svg' || input === prefix + '.png' || input === prefix + '.metrics.json') throw new Error('Output would overwrite input.');
  const launch = opts['puppeteer-config'] ? JSON.parse(readFileSync(resolve(opts['puppeteer-config']), 'utf8')) : {};
  if (!launch.executablePath && !launch.channel) launch.executablePath = existingBrowser(puppeteer);
  const temp = mkdtempSync(join(tmpdir(), 'mermaid-design-'));
  let browser;
  try {
    const svgPath = join(temp, 'diagram.svg');
    const command = ['-i', input, '-o', svgPath, '-w', String(Math.round(width)), '-b', 'white', '-q'];
    const launchPath = join(temp, 'browser.json');
    writeFileSync(launchPath, JSON.stringify(launch));
    command.push('-p', launchPath);
    execFileSync(cli, command, { encoding: 'utf8', timeout: 60000, stdio: ['ignore', 'pipe', 'pipe'] });
    const svg = readFileSync(svgPath, 'utf8');
    browser = await puppeteer.launch(launch);
    const page = await browser.newPage();
    await page.setViewport({ width: Math.ceil(width), height: 900, deviceScaleFactor: 2 });
    await page.setJavaScriptEnabled(false);
    await page.setContent('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:white}svg{display:block}</style></head><body>' + svg + '</body></html>');
    await page.evaluate(() => document.fonts.ready);
    const report = await page.evaluate((targetWidth) => {
      const root = document.querySelector('svg');
      if (!root) throw new Error('CLI did not produce an SVG.');
      const vb = root.viewBox.baseVal;
      const nativeWidth = vb.width, nativeHeight = vb.height;
      if (!(nativeWidth > 0 && nativeHeight > 0)) throw new Error('Invalid SVG viewBox.');
      const scale = Math.min(1, targetWidth / nativeWidth);
      root.style.maxWidth = 'none';
      root.style.width = `${nativeWidth * scale}px`;
      root.style.height = `${nativeHeight * scale}px`;
      root.setAttribute('width', String(nativeWidth * scale));
      root.setAttribute('height', String(nativeHeight * scale));
      const round = v => Math.round(v * 100) / 100;
      const bounds = el => { const b = el.getBoundingClientRect(); return { x: b.x, y: b.y, width: b.width, height: b.height }; };
      const fonts = el => [...el.querySelectorAll('text, foreignObject .nodeLabel, foreignObject .edgeLabel')].filter(e => e.textContent.trim()).map(e => {
        const matrix = typeof e.getScreenCTM === 'function' ? e.getScreenCTM() : root.getScreenCTM();
        const s = matrix ? Math.hypot(matrix.a, matrix.b) : scale;
        return round(parseFloat(getComputedStyle(e).fontSize) * s);
      }).filter(Number.isFinite);
      const nodes = [...root.querySelectorAll('g.node')].map(node => {
        const shape = node.querySelector(':scope > rect, :scope > polygon, :scope > path, :scope > circle, :scope > ellipse');
        const label = node.querySelector('g.label');
        const b = bounds(shape || node), l = label ? bounds(label) : null;
        return {
          id: node.id,
          text: (label || node).textContent.replace(/\s+/g, ' ').trim(),
          shapeWidth: round(b.width / scale), shapeHeight: round(b.height / scale),
          aspectRatio: round(b.width / b.height),
          labelBoxAreaRatio: l && b.width * b.height ? round(l.width * l.height / (b.width * b.height)) : null,
          effectiveFontPx: fonts(node),
          screenBounds: b,
        };
      });
      if (!nodes.length) throw new Error('No flowchart nodes found. This helper supports flowcharts.');
      const overlappingNodePairs = [];
      for (let i = 0; i < nodes.length; i++) for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i].screenBounds, b = nodes[j].screenBounds;
        if (Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>1 && Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>1) overlappingNodePairs.push([nodes[i].id,nodes[j].id]);
      }
      const allFonts = nodes.flatMap(n => n.effectiveFontPx);
      const minimumEffectiveNodeFontPx = allFonts.length ? Math.min(...allFonts) : null;
      const edgeFonts = [...root.querySelectorAll('g.edgeLabel')].flatMap(fonts);
      const warnings = [];
      if (minimumEffectiveNodeFontPx === null) warnings.push('Node text size could not be measured; inspect manually.');
      else if (minimumEffectiveNodeFontPx < 14) warnings.push('Effective node font is below 14 CSS px at target width; review layout before reducing font size.');
      if (edgeFonts.length && Math.min(...edgeFonts) < 14) warnings.push('Effective edge-label font is below 14 CSS px; inspect branch readability.');
      const sparse = nodes.filter(n => n.aspectRatio < 1.6 && n.labelBoxAreaRatio !== null && n.labelBoxAreaRatio < 0.4);
      if (sparse.length) warnings.push(`Review ${sparse.length} near-square/sparse nodes. This is shape-dependent, not an aesthetic failure by itself.`);
      if (overlappingNodePairs.length) warnings.push('Node bounding boxes overlap; inspect the image.');
      return { targetWidth, nativeWidth: round(nativeWidth), nativeHeight: round(nativeHeight), displayScale: round(scale), displayWidth: round(nativeWidth*scale), displayHeight: round(nativeHeight*scale), minimumEffectiveNodeFontPx, minimumEffectiveEdgeFontPx: edgeFonts.length ? Math.min(...edgeFonts) : null, nodes, overlappingNodePairs, warnings,
        reviewNotice: 'Geometry report does not certify aesthetics, semantics, font glyph coverage, edge crossings, text clipping, or compatibility with a different host. Open the PNG at its intended CSS size.' };
    }, width);
    const direction=readFileSync(input,'utf8').match(/^\s*(?:flowchart|graph)\s+(TB|TD|BT|LR|RL)\b/m)?.[1] || 'TB';
    const layout=opts.layout ? await page.evaluate(extractLayout,{title:basename(input,'.mmd'),direction}) : null;
    if(formats.has('png')) await page.$('svg').then(el => el.screenshot({ path: join(temp, 'diagram.png') }));
    if(formats.has('pdf')) {
      // Print the SVG directly: no canvas or bitmap conversion, and no fitting
      // to the preview viewport. A single native-size page preserves long graphs.
      const size = await page.evaluate(() => {
        const root = document.querySelector('svg');
        const {width, height} = root.viewBox.baseVal;
        return {width: Math.ceil(width), height: Math.ceil(height)};
      });
      // PDF 1.x readers commonly enforce 14,400 points (200 inches) per side.
      // Reject larger diagrams rather than silently clipping or shrinking them.
      const maxCssPixels = 200 * 96;
      if(size.width > maxCssPixels || size.height > maxCssPixels) {
        throw new Error(`PDF page exceeds the 200-inch maximum (19200 CSS pixels per side): ${size.width} x ${size.height}. Split the diagram before exporting PDF.`);
      }
      await page.evaluate(({width, height}) => {
        const root = document.querySelector('svg');
        root.style.width = `${width}px`;
        root.style.height = `${height}px`;
        root.setAttribute('width', String(width));
        root.setAttribute('height', String(height));
        const style = document.createElement('style');
        style.textContent = `@page {size: ${width}px ${height}px; margin: 0} html,body {margin:0; padding:0; width:${width}px; height:${height}px; overflow:hidden; print-color-adjust:exact; -webkit-print-color-adjust:exact}`;
        document.head.appendChild(style);
      }, size);
      await page.pdf({path: join(temp, 'diagram.pdf'), width: `${size.width}px`, height: `${size.height}px`, margin: {top:0,right:0,bottom:0,left:0}, printBackground: true, preferCSSPageSize: true, displayHeaderFooter: false, scale: 1});
    }
    const version = execFileSync(cli, ['--version'], { encoding: 'utf8', timeout: 10000 }).trim();
    report.renderer = { cliVersion: version, browserVersion: await browser.version(), deviceScaleFactor: 2 };
    mkdirSync(dirname(prefix), { recursive: true });
    if(formats.has('svg')) copyFileSync(svgPath, prefix + '.svg');
    if(formats.has('png')) copyFileSync(join(temp, 'diagram.png'), prefix + '.png');
    if(formats.has('pdf')) copyFileSync(join(temp, 'diagram.pdf'), prefix + '.pdf');
    if(layout) {
      const target=resolve(opts.layout);
      if(target===input) throw new Error('Layout output would overwrite source.');
      mkdirSync(dirname(target),{recursive:true});
      writeFileSync(target,JSON.stringify(layout,null,2)+'\n');
    }
    writeFileSync(prefix + '.metrics.json', JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify({ pdf: formats.has('pdf') ? prefix+'.pdf':null, svg: formats.has('svg') ? prefix+'.svg':null, png:formats.has('png') ? prefix+'.png':null, layout:opts.layout ? resolve(opts.layout):null, metrics: prefix+'.metrics.json', ...report.renderer, nativeSize: [report.nativeWidth, report.nativeHeight], displaySize: [report.displayWidth, report.displayHeight], minimumEffectiveNodeFontPx: report.minimumEffectiveNodeFontPx, warnings: report.warnings }, null, 2));
  } finally {
    if (browser) await browser.close();
    rmSync(temp, { recursive: true, force: true });
  }
}

main().catch(error => {
  console.error(error.stderr?.toString() || error.message || String(error));
  process.exitCode = 1;
});
