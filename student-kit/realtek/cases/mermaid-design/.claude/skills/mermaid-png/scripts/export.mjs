#!/usr/bin/env node
import {execFileSync} from 'node:child_process';
import {mkdtempSync,mkdirSync,readFileSync,writeFileSync,copyFileSync,rmSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {dirname,join,basename,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const help=`Export related Mermaid flowcharts as PNG, SVG, PDF, and native editable PowerPoint.
Usage: node export.mjs input.mmd [related.mmd ...] --out output-prefix
  --formats png,svg,pdf,pptx Select formats; default: png,svg,pptx
  --pages auto|single|groups Default: auto (split large grouped diagrams)
  --orientation auto|landscape|portrait  Default: auto, one size per deck
  --width CSS_PX            Preview container width, default 760
  --python EXECUTABLE       Python with python-pptx, default python3
  --mmdc EXECUTABLE         Existing Mermaid CLI, default mmdc
  --puppeteer-config FILE   Existing browser launch settings
Multiple input files are treated as ONE related task, in the supplied order.
PDF is one native-size vector page per input diagram (maximum 200 inches per side).
PowerPoint output is .pptx, never a renamed legacy .ppt. No packages are auto-installed.`;

function run() {
  const argv=process.argv.slice(2);
  if(argv.includes('--help') || argv.includes('-h')) {console.log(help);return;}
  const opts={formats:'png,svg,pptx',pages:'auto',orientation:'auto',width:'760',python:'python3',mmdc:'mmdc'};
  const keys=new Set([...Object.keys(opts),'out','puppeteer-config']),inputs=[];
  while(argv.length) {
    const a=argv.shift();
    if(a.startsWith('--')) {
      if(!keys.has(a.slice(2)) || !argv.length) throw new Error(`Invalid option ${a}\n${help}`);
      opts[a.slice(2)]=argv.shift();
    } else inputs.push(resolve(a));
  }
  if(!inputs.length || !opts.out) throw new Error(help);
  const formats=new Set(opts.formats.split(','));
  if(!formats.size || [...formats].some(f=>!['png','svg','pdf','pptx'].includes(f))) throw new Error('--formats must select png,svg,pdf,pptx.');
  if(!['auto','single','groups'].includes(opts.pages)) throw new Error('Invalid --pages.');
  if(!['auto','landscape','portrait'].includes(opts.orientation)) throw new Error('Invalid --orientation.');
  const prefix=resolve(opts.out);
  if(/\.(ppt|pptx|png|svg|pdf)$/i.test(prefix)) throw new Error('--out is a prefix without an extension; legacy .ppt is not supported. Use --formats pptx.');
  for(const p of inputs) if(!existsSync(p) || !/\.mmd$/i.test(p)) throw new Error(`Input must be an existing .mmd: ${p}`);
  const here=dirname(fileURLToPath(import.meta.url)),temp=mkdtempSync(join(tmpdir(),'mermaid-export-'));
  try {
    if(formats.has('pptx')) {
      try {execFileSync(opts.python,['-c','import pptx'],{stdio:'pipe',timeout:10000});}
      catch {throw new Error(`Python '${opts.python}' needs python-pptx. Install it in your chosen environment, then pass --python; no packages were installed.`);}
    }
    const assets=[],layouts=[],staged=[];
    for(let i=0;i<inputs.length;i++) {
      const stem=basename(inputs[i],'.mmd').replace(/[^\p{L}\p{N}_-]/gu,'-');
      const filePrefix=inputs.length===1 ? prefix : `${prefix}-${String(i+1).padStart(2,'0')}-${stem}`;
      const sourceOutput=filePrefix+'.mmd';
      if(sourceOutput!==inputs[i] && existsSync(sourceOutput) && !readFileSync(sourceOutput).equals(readFileSync(inputs[i]))) {
        throw new Error(`Refusing to overwrite a different Mermaid source: ${sourceOutput}. Choose another --out prefix.`);
      }
      const imageFormats=[...formats].filter(f=>f!=='pptx');
      const tmpPrefix=join(temp,`diagram-${i}`),layout=tmpPrefix+'.layout.json';
      const args=[join(here,'render.mjs'),inputs[i],'--out',tmpPrefix,'--width',opts.width,'--mmdc',opts.mmdc,'--formats',imageFormats.length?imageFormats.join(','):'svg'];
      if(formats.has('pptx')) args.push('--layout',layout);
      if(opts['puppeteer-config']) args.push('--puppeteer-config',resolve(opts['puppeteer-config']));
      execFileSync(process.execPath,args,{stdio:'pipe',timeout:120000});
      const metrics=JSON.parse(readFileSync(tmpPrefix+'.metrics.json','utf8'));
      const item={source:basename(inputs[i]),outputs:{mmd:filePrefix+'.mmd'},warnings:metrics.warnings};
      if(filePrefix+'.mmd'!==inputs[i]) {
        const stagedSource=join(temp,`source-${i}.mmd`);
        copyFileSync(inputs[i],stagedSource);
        staged.push([stagedSource,filePrefix+'.mmd']);
      }
      for(const f of imageFormats) {staged.push([tmpPrefix+'.'+f,filePrefix+'.'+f]);item.outputs[f]=filePrefix+'.'+f;}
      assets.push(item);layouts.push(layout);
    }
    let pptxReport=null;
    if(formats.has('pptx')) {
      const deck=join(temp,'deck.pptx');
      try {execFileSync(opts.python,[join(here,'native_pptx.py'),...layouts,'--out',deck,'--pages',opts.pages,'--orientation',opts.orientation],{stdio:'pipe',timeout:120000});}
      catch(e) {throw new Error(e.stderr?.toString() || e.message);}
      pptxReport=JSON.parse(readFileSync(deck+'.report.json','utf8'));
      const temporarySources=pptxReport.inputs || [];
      pptxReport.inputs=assets.map(a=>a.outputs.mmd);
      pptxReport.inputType='mermaid';
      for(const slide of pptxReport.slides) slide.source=assets[slide.inputIndex].outputs.mmd;
      pptxReport.warnings=pptxReport.warnings.map(w=>temporarySources.reduce((text,p,i)=>text.split(p).join(assets[i].source),w));
      staged.push([deck,prefix+'.pptx']);
      // Keep source paths in private intermediates, not the public manifest.
    }
    const destinations=staged.map(([,p])=>p);
    if(destinations.some(p=>inputs.includes(p))) throw new Error('Output would overwrite a Mermaid input.');
    for(const [from,to] of staged) {mkdirSync(dirname(to),{recursive:true});copyFileSync(from,to);}
    const report={formats:[...formats],inputs:assets,pptx:formats.has('pptx')?prefix+'.pptx':null,presentation:pptxReport,reviewNotice:'Inspect exported images and slides. Native shapes are editable, but editability does not imply automatic connection rerouting after moving a node.'};
    mkdirSync(dirname(prefix),{recursive:true});
    writeFileSync(prefix+'.export.json',JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify({manifest:prefix+'.export.json',files:destinations,...(pptxReport?{presentation:pptxReport}:{})},null,2));
  } finally {rmSync(temp,{recursive:true,force:true});}
}
try {run();} catch(e) {console.error(e.stderr?.toString() || e.message || String(e));process.exitCode=1;}
