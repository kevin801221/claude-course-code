/** Runs inside the render browser. All coordinates use the original SVG viewBox. */
export function extractLayout(options) {
  const fallbackTitle=typeof options==='string' ? options:options.title;
  const direction=typeof options==='string' ? 'TB':options.direction;
  const root = document.querySelector('svg');
  if (!root) throw new Error('No SVG to extract.');
  if (root.querySelector('image, foreignObject img')) throw new Error('Native PowerPoint export does not support embedded diagram images. Use text and flowchart shapes; no flattened fallback was created.');
  const inverse = root.getScreenCTM().inverse();
  const round = n => Math.round(n * 1000) / 1000;
  const strokeWidth = value => { const n=parseFloat(value); return Number.isFinite(n) ? n:1; };
  const toNative = (x, y) => {
    const p = new DOMPoint(x, y).matrixTransform(inverse);
    return [round(p.x), round(p.y)];
  };
  const box = el => {
    const r = el.getBoundingClientRect();
    const a = toNative(r.left, r.top), b = toNative(r.right, r.bottom);
    return { x: a[0], y: a[1], width: round(b[0]-a[0]), height: round(b[1]-a[1]) };
  };
  const color = (value, fallback = '#1E293B') => {
    if (!value || value === 'none' || value === 'transparent') return 'transparent';
    const m = value.match(/rgba?\(\s*([\d.]+)[, ]+([\d.]+)[, ]+([\d.]+)(?:\s*[,/]\s*([\d.]+))?\s*\)/);
    if (m) return m[4] === '0' ? 'transparent' : '#'+m.slice(1,4).map(v => Math.round(Number(v)).toString(16).padStart(2,'0')).join('').toUpperCase();
    return /^#[0-9a-f]{6}$/i.test(value) ? value : fallback;
  };
  const labelText = el => {
    if (!el) return '';
    const html = el.querySelector('foreignObject .nodeLabel, foreignObject .edgeLabel, foreignObject div');
    if (html) return html.innerText.trim();
    const outer = [...el.querySelectorAll('text > tspan')];
    if (outer.length) return outer.map(t => t.textContent).join('\n').trim();
    return el.textContent.trim();
  };
  const labelStyle = el => {
    const text = el?.querySelector('text, foreignObject .nodeLabel, foreignObject .edgeLabel, foreignObject div') || el || root;
    const s = getComputedStyle(text);
    return { fontSize: parseFloat(s.fontSize) || 16, fontFamily: s.fontFamily, color: color(text.tagName.toLowerCase()==='text' ? s.fill : s.color) };
  };
  const contains = (a,b) => b.x>=a.x-1 && b.y>=a.y-1 && b.x+b.width<=a.x+a.width+1 && b.y+b.height<=a.y+a.height+1;
  const groups = [...root.querySelectorAll('g.cluster')].map(el => {
    const rect = el.querySelector(':scope > rect');
    if (!rect) throw new Error(`Cannot extract group ${el.id}.`);
    const s = getComputedStyle(rect), label = el.querySelector('.cluster-label');
    return { id: el.id, title: labelText(label), ...box(rect), fill: color(s.fill), stroke: color(s.stroke), fontSize: labelStyle(label).fontSize, parentId: null };
  });
  for (const g of groups) {
    const parent = groups.filter(p=>p.id!==g.id && p.width*p.height>g.width*g.height+1 && contains(p,g)).sort((a,b)=>a.width*a.height-b.width*b.height)[0];
    g.parentId = parent?.id || null;
  }
  // Mermaid's SVG paint order is not workflow order (often the reverse).
  // Retain the diagram's declared reading direction when turning groups into pages.
  groups.sort((a,b)=> ['LR','RL'].includes(direction) ? (direction==='RL'?-1:1)*(a.x-b.x) || a.y-b.y : (direction==='BT'?-1:1)*(a.y-b.y) || a.x-b.x);
  const samplePath = path => {
    const length = path.getTotalLength(), matrix = path.getScreenCTM();
    if (!Number.isFinite(length) || length === 0) throw new Error(`Empty path ${path.id}.`);
    const count = Math.min(1500, Math.max(2,Math.ceil(length/3)));
    const points = [];
    for(let i=0;i<=count;i++) {
      const p = path.getPointAtLength(length*i/count).matrixTransform(matrix);
      points.push(toNative(p.x,p.y));
    }
    // Douglas-Peucker keeps straight edges compact and approximates curves to 0.4 SVG px.
    const simplify = pts => {
      if(pts.length<=2) return pts;
      const a=pts[0], b=pts.at(-1), dx=b[0]-a[0], dy=b[1]-a[1], norm=dx*dx+dy*dy;
      let max=0,index=0;
      for(let i=1;i<pts.length-1;i++) {
        const t=norm ? Math.max(0,Math.min(1,((pts[i][0]-a[0])*dx+(pts[i][1]-a[1])*dy)/norm)) : 0;
        const d=Math.hypot(pts[i][0]-a[0]-t*dx,pts[i][1]-a[1]-t*dy);
        if(d>max){max=d;index=i;}
      }
      return max>0.4 ? [...simplify(pts.slice(0,index+1)).slice(0,-1),...simplify(pts.slice(index))] : [a,b];
    };
    return simplify(points);
  };
  const nodes = [...root.querySelectorAll('g.node')].map(el => {
    const shape=el.querySelector(':scope > rect, :scope > polygon, :scope > path, :scope > circle, :scope > ellipse');
    if(!shape) throw new Error(`Unsupported native node ${el.id}. Use classic flowchart shapes.`);
    const s=getComputedStyle(shape), tag=shape.tagName.toLowerCase(), label=el.querySelector('g.label');
    let kind=tag==='rect' ? (parseFloat(shape.getAttribute('rx') || s.rx)>0 ? 'roundRect':'rect') : ['circle','ellipse'].includes(tag) ? 'ellipse' : tag==='polygon' ? 'polygon':'path';
    let points;
    if(tag==='polygon') points=[...shape.points].map(p=> {const q=p.matrixTransform(shape.getScreenCTM());return toNative(q.x,q.y);});
    if(tag==='path') points=samplePath(shape);
    const b=box(shape);
    return {id:el.id.replace(/^flowchart-/,'').replace(/-\d+$/,''),kind,...b,text:labelText(label),...labelStyle(label),fill:color(s.fill),stroke:color(s.stroke),strokeWidth:strokeWidth(s.strokeWidth),groupIds:groups.filter(g=>contains(g,b)).map(g=>g.id),...(points?{points}:{})};
  });
  const objects=[...nodes,...groups], ids=objects.map(o=>o.id);
  const borderDistance = (p,b) => {
    const dx=Math.max(b.x-p[0],0,p[0]-b.x-b.width),dy=Math.max(b.y-p[1],0,p[1]-b.y-b.height);
    if(dx || dy) return Math.hypot(dx,dy);
    return Math.min(p[0]-b.x,b.x+b.width-p[0],p[1]-b.y,b.y+b.height-p[1]);
  };
  const inferEndpoint = p => {
    const choices=objects.map(o=>({id:o.id,d:borderDistance(p,o)})).sort((a,b)=>a.d-b.d);
    if(!choices.length || choices[0].d>16 || (choices[1] && Math.abs(choices[1].d-choices[0].d)<0.05)) throw new Error('Cannot unambiguously resolve an edge endpoint. Use simple unique node ids or split the diagram.');
    return choices[0].id;
  };
  const labels=[...root.querySelectorAll('g.edgeLabels > g.edgeLabel')];
  const paths=[...root.querySelectorAll('g.edgePaths > path')];
  const edges=paths.map((path,index)=>{
    // Hidden layout edges still occupy a position in edgeLabels. Filter only
    // after preserving that original index, or visible conditions shift.
    if(!path.classList.contains('flowchart-link')) return null;
    const points=samplePath(path),s=getComputedStyle(path),pairs=[];
    for(const source of ids) for(const target of ids) {
      const prefix=`L_${source}_${target}_`;
      if(path.id.startsWith(prefix) && /^\d+$/.test(path.id.slice(prefix.length))) pairs.push([source,target]);
    }
    let source,target;
    if(pairs.length===1) [source,target]=pairs[0];
    else {source=inferEndpoint(points[0]);target=inferEndpoint(points.at(-1));}
    const markerStart=path.getAttribute('marker-start') || s.markerStart, markerEnd=path.getAttribute('marker-end') || s.markerEnd;
    for(const marker of [markerStart,markerEnd]) if(marker && marker!=='none' && !/point(?:Start|End)/i.test(marker)) throw new Error('Native PPTX export currently supports plain arrowheads; circle/cross arrowheads require an explicit native implementation.');
    const el=labels[index],text=labelText(el);
    return {id:path.id,source,target,points,stroke:color(s.stroke,'#94A3B8'),strokeWidth:strokeWidth(s.strokeWidth),dash:s.strokeDasharray!=='none' && s.strokeDasharray!=='0px',arrowStart:!!markerStart && markerStart!=='none',arrowEnd:!!markerEnd && markerEnd!=='none',label:text ? {text,...box(el.querySelector('g.label') || el),...labelStyle(el),fill:'#FFFFFF'} : null};
  }).filter(Boolean);
  const vb=root.viewBox.baseVal;
  return {schemaVersion:1,title:root.querySelector(':scope > title')?.textContent || fallbackTitle,viewBox:{x:vb.x,y:vb.y,width:vb.width,height:vb.height},nodes,edges,groups,notes:['Curved edges are editable native polyline approximations within 0.4 SVG px.']};
}
