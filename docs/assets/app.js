/* Environment Observatory — zero-dependency static client, data-only rendering via textContent. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const pages = new Set(['overview','skills','packages','tools','risks','method']);
  const names = {overview:'Overview',skills:'Skills Registry',packages:'Package Inventory',tools:'Tool Interfaces',risks:'Risk Register',method:'Methodology'};
  let catalog = null;
  const state = { skills:{page:1,search:'',filter:'all'}, packages:{page:1,search:'',filter:'all'}, tools:{page:1,search:'',filter:'all'} };
  const PAGE_SIZE = 15;
  function element(tag, className='', value='') { const n=document.createElement(tag); if(className)n.className=className; if(value!==undefined)n.textContent=String(value); return n; }
  function td(value, className='') { return element('td',className,value); }
  function selectPage() {
    const page=(location.hash.slice(1).split('?')[0]||'overview'); const key=pages.has(page)?page:'overview';
    document.querySelectorAll('.page').forEach(n=>n.classList.toggle('active',n.id===key));
    document.querySelectorAll('.nav-link').forEach(n=>{const yes=n.dataset.page===key; n.classList.toggle('active',yes); if(yes)n.setAttribute('aria-current','page');else n.removeAttribute('aria-current');});
    $('currentPageName').textContent=names[key]; $('sidebar').classList.remove('open'); window.scrollTo({top:0,behavior:'instant'});
  }
  function toDisplayText(s){return String(s??'').toLowerCase();}
  function renderTable(kind) {
    if(!catalog)return;
    const st=state[kind]; const source=catalog[kind];
    const rows=source.filter(item=> {
      const field=kind==='skills'?item.origin:kind==='tools'?item.namespace:item.ecosystem;
      return (st.filter==='all'||field===st.filter) && Object.values(item).some(x=>toDisplayText(x).includes(st.search));
    });
    const total=Math.max(1,Math.ceil(rows.length/PAGE_SIZE)); st.page=Math.min(Math.max(st.page,1),total);
    const subset=rows.slice((st.page-1)*PAGE_SIZE,st.page*PAGE_SIZE);
    const body=$(kind+'Rows'); const frag=document.createDocumentFragment();
    for(const item of subset){const tr=document.createElement('tr');
      if(kind==='skills'){
        tr.append(td(item.name,'mono'),td(item.origin)); tr.append(td(item.category));
        const mark=td('');mark.append(element('span','chip '+(item.evidence==='filesystem'?'green':'purple'),item.evidence));tr.append(mark);tr.append(td(item.publish));
      }else if(kind==='packages'){
        tr.append(td(item.name,'mono'),td(item.version,'mono')); const c=td('');c.append(element('span','chip',item.ecosystem));tr.append(c);
      }else{
        tr.append(td(item.name,'mono'),td(item.namespace));const c=td('');c.append(element('span','chip gold','Advertised only'));tr.append(c);
      }
      frag.append(tr);
    }
    body.replaceChildren(frag); $(kind+'Empty').hidden=rows.length>0;
    $(kind+'Count').textContent=`${rows.length.toLocaleString('zh-CN')} 条结果 · 每页 ${PAGE_SIZE} 条`;
    $(kind+'Page').textContent=`${st.page} / ${total}`;
    $(kind+'Prev').disabled=st.page===1; $(kind+'Next').disabled=st.page===total;
  }
  function controls(kind){
    $(kind+'Search').addEventListener('input',event=>{state[kind].search=event.target.value.toLowerCase().trim();state[kind].page=1;renderTable(kind);});
    $(kind+'Filter').addEventListener('change',event=>{state[kind].filter=event.target.value;state[kind].page=1;renderTable(kind);});
    $(kind+'Prev').addEventListener('click',()=>{state[kind].page-=1;renderTable(kind);});
    $(kind+'Next').addEventListener('click',()=>{state[kind].page+=1;renderTable(kind);});
  }
  function renderBars(groups){
    const top=[...groups].sort((a,b)=>b.count-a.count).slice(0,7);const max=top[0].count;
    const fragment=document.createDocumentFragment();
    for(const r of top){const line=element('div','bar-row','');const lab=element('label','',r.namespace.replaceAll('_',' '));lab.title=r.namespace;
      const track=element('div','bar-track','');const fill=element('div','bar-fill','');fill.style.width=(r.count/max*100).toFixed(2)+'%';track.append(fill);
      line.append(lab,track,element('span','bar-num',r.count));fragment.append(line);
    } $('connectorBars').replaceChildren(fragment);
  }
  function renderEcosystems(groups){const fragment=document.createDocumentFragment();
    for(const row of groups){const item=element('div','ecosystem-chip',''); item.append(element('b','',row.count.toLocaleString('en-US')),element('span','',row.name));fragment.append(item);}
    $('ecosystemStrip').replaceChildren(fragment);
  }
  function renderRisks(risks){const fragment=document.createDocumentFragment();
    for(const item of risks){const node=element('article','risk-card',''); const left=element('div','risk-id',item.id);const body=element('div','risk-content','');
      const head=element('div','risk-head','');head.append(element('h3','',item.title),element('span','risk-sev '+item.severity,item.severity+' / '+item.level));
      body.append(head,element('p','',`${item.domain} · ${item.evidence}`),element('div','mitigation','↳ '+item.mitigation));node.append(left,body);fragment.append(node);
    } $('riskCards').replaceChildren(fragment);
  }
  async function init(){
    try{
      const response=await fetch('data/catalog.json',{cache:'no-cache'});
      if(!response.ok)throw new Error('HTTP '+response.status);
      catalog=await response.json();
      if(!Array.isArray(catalog.skills)||!Array.isArray(catalog.packages)||!Array.isArray(catalog.tools))throw new Error('Invalid catalog data');
      renderBars(catalog.tool_groups);renderEcosystems(catalog.package_groups);renderRisks(catalog.risks);
      const select=$('toolsFilter');for(const g of catalog.tool_groups){const option=document.createElement('option');option.value=g.namespace;option.textContent=g.namespace;select.append(option);}
      for(const kind of ['skills','packages','tools']){controls(kind);renderTable(kind);}
    }catch(error){
      const alert=element('div','callout','数据目录未能加载：'+error.message+'。请通过 HTTP 服务预览 docs/ 文件夹，并确保 data/catalog.json 存在。');
      $('overview').prepend(alert);
      for(const kind of ['skills','packages','tools']){$(kind+'Count').textContent='Catalog unavailable';}
    }
  }
  const stored=(()=>{try{return localStorage.getItem('envatlas_theme')}catch(e){return null}})();
  if(stored==='light'||stored==='dark')document.documentElement.dataset.theme=stored;
  $('themeButton').addEventListener('click',()=>{
    const next=document.documentElement.dataset.theme==='light'?'dark':'light';document.documentElement.dataset.theme=next;
    try{localStorage.setItem('envatlas_theme',next)}catch(e){};
  });
  $('menuButton').addEventListener('click',()=>$('sidebar').classList.toggle('open'));
  window.addEventListener('hashchange',selectPage);selectPage();init();
})();
