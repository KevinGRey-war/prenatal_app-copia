'use strict';
const $=id=>document.getElementById(id), E=GameEngine;
let stages=[],state=E.fresh(),session='',paused=false,emotionTimer,lastHeight=0,voiceGeneration=0;
function post(type,extra={}){window.parent.postMessage({isStreamlitMessage:true,type,...extra},'*');}
function resize(){const h=Math.ceil($('game').getBoundingClientRect().height)+4;if(h!==lastHeight){lastHeight=h;post('streamlit:setFrameHeight',{height:h});}}
new ResizeObserver(resize).observe($('game'));
function save(){try{sessionStorage.setItem('vida-game-'+session,JSON.stringify(state));}catch(_){}}
function stopVoice(){voiceGeneration++;if('speechSynthesis'in window)window.speechSynthesis.cancel();Music.duck(false);}
function speak(text){
  stopVoice();if(!('speechSynthesis'in window))return;
  const generation=voiceGeneration,parts=text.match(/[^.!?]+[.!?]?/g)||[text];let i=0;
  Music.duck(true);
  function next(){if(generation!==voiceGeneration)return;if(i>=parts.length){Music.duck(false);return;}
    const utterance=new SpeechSynthesisUtterance(parts[i++]);utterance.lang='es-ES';utterance.rate=.96;
    const voice=speechSynthesis.getVoices().find(v=>v.lang.startsWith('es'));if(voice)utterance.voice=voice;
    utterance.onend=next;utterance.onerror=()=>Music.duck(false);speechSynthesis.speak(utterance);
  }next();
}
function musicLabel(){$('music').textContent=Music.playing?'♫ Silenciar':'♫ Música';$('music').setAttribute('aria-pressed',String(Music.playing));}
function art(stage){
  const defs='<defs><radialGradient id="bubble"><stop stop-color="#fff8f0"/><stop offset="1" stop-color="#eabfd6"/></radialGradient><linearGradient id="skin" x2="1" y2="1"><stop stop-color="#ffddb9"/><stop offset="1" stop-color="#efb78e"/></linearGradient></defs>';
  if(stage===0)return `<svg viewBox="0 0 300 260" aria-hidden="true">${defs}<ellipse cx="150" cy="130" rx="106" ry="112" fill="url(#bubble)" stroke="#fff7" stroke-width="9"/><path d="M177 181C135 220 86 179 92 141C99 111 139 112 140 140" fill="none" stroke="#cf87a1" stroke-width="10" stroke-linecap="round"/><g transform="rotate(-25 150 130)"><path class="skin" d="M163 72C109 50 82 107 114 141C127 155 145 150 145 169C143 187 164 192 179 174C198 148 169 137 172 123C197 111 194 84 163 72Z" fill="url(#skin)" stroke="#d59b84" stroke-width="2"/><circle cx="136" cy="101" r="4" fill="#64505c"/><ellipse cx="153" cy="143" rx="14" ry="8" fill="#f4c4a3"/><circle cx="171" cy="166" r="9" fill="#f4c4a3"/></g><circle cx="80" cy="60" r="5" fill="#fff"/><circle cx="217" cy="177" r="4" fill="#fff"/></svg>`;
  if(stage<4){const scale=stage===1?.78:stage===2?.93:1;
    return `<svg viewBox="0 0 300 260" aria-hidden="true">${defs}<ellipse cx="150" cy="130" rx="111" ry="119" fill="url(#bubble)" stroke="#fff8" stroke-width="8"/><path d="M162 160C112 219 61 172 89 151" fill="none" stroke="#c78ba8" stroke-width="8" stroke-linecap="round"/><g transform="translate(${150*(1-scale)} ${130*(1-scale)}) scale(${scale}) rotate(-18 150 130)"><ellipse class="skin" cx="153" cy="156" rx="45" ry="57" fill="url(#skin)"/><circle class="skin" cx="145" cy="88" r="46" fill="url(#skin)" stroke="#d9a28c" stroke-width="2"/><path d="M113 85q9 9 18 0M149 85q9 9 18 0" fill="none" stroke="#74505a" stroke-width="3" stroke-linecap="round"/><path d="M133 106q10 6 19 0" fill="none" stroke="#b76c75" stroke-width="3" stroke-linecap="round"/><ellipse cx="119" cy="101" rx="10" ry="6" fill="#efa0a0" opacity=".6"/><path class="skin" d="M177 138q-28 22-43 5M170 192q-21 21-39 0" fill="none" stroke="#efbd9b" stroke-width="20" stroke-linecap="round"/><ellipse class="skin" cx="128" cy="190" rx="12" ry="9" fill="#f5c5a1"/><path d="M123 51q24-18 43 2" fill="none" stroke="#8b6557" stroke-width="5" stroke-linecap="round"/></g></svg>`;
  }
  return `<svg viewBox="0 0 300 260" aria-hidden="true">${defs}<ellipse cx="150" cy="238" rx="86" ry="12" fill="#c89ab82b"/><path d="M91 126Q55 220 150 243Q245 220 209 126Z" fill="#dfc5ed" stroke="#bc91cf" stroke-width="2"/><path d="M92 145L199 219M210 145L106 219" stroke="#fff8" stroke-width="12"/><circle class="skin" cx="150" cy="92" r="60" fill="url(#skin)" stroke="#d9a28c" stroke-width="2"/><circle cx="127" cy="91" r="5" fill="#594854"/><circle cx="172" cy="91" r="5" fill="#594854"/><ellipse cx="113" cy="108" rx="12" ry="7" fill="#ed9ca4" opacity=".7"/><ellipse cx="187" cy="108" rx="12" ry="7" fill="#ed9ca4" opacity=".7"/><path d="M137 116q13 17 26 0" fill="#c06b7e"/><path d="M126 37q17-20 31-1q-10-5-13 5" fill="#8c6354"/><path class="tear" d="M119 99q-17 24 0 24q17 0 0-24M179 99q-17 24 0 24q17 0 0-24" fill="#8fc8e4"/><path d="M132 183q18-23 36 0q-18 30-36 0" fill="#fff4fa"/></svg>`;
}
function render(){
  $('intro').hidden=state.started;$('board').hidden=!state.started||state.done;$('summary').hidden=!state.done;
  $('pause').disabled=!state.started||state.done;
  if(!state.started){resize();return;}
  const s=stages[state.stage],stats=E.stats(state,stages);
  $('correct').textContent=stats.good;$('errors').textContent=stats.errors;$('risk').textContent=E.risk(stats.errors);
  $('timeline').replaceChildren(...stages.map((stage,i)=>{const li=document.createElement('li');li.className=i===state.stage?'active':i<state.stage?'complete':'';
    const icon=document.createElement('b');icon.textContent=i<state.stage?'✓':stage.icon;li.append(icon,document.createTextNode(stage.name));if(i===state.stage)li.setAttribute('aria-current','step');return li;}));
  $('weeks').textContent=s.weeks;$('stageTitle').textContent=s.name;$('focus').textContent=s.focus;
  $('illustration').innerHTML=art(state.stage);$('illustration').setAttribute('aria-label',s.short+'; ilustración educativa');
  $('illustration').style.transform=`scale(${.88+.12*stats.stageGood/stats.target})`;
  $('figureLabel').textContent=s.short;$('growth').max=stats.target;$('growth').value=stats.stageGood;
  $('progressLabel').textContent=`Aprendizaje de la etapa: ${stats.stageGood} de ${stats.target} elecciones adecuadas`;
  $('recipientHint').textContent=state.stage<4?'🤰 Elige alimentos para mamá. Sus nutrientes llegan al bebé.':'🤱 Revisa la etiqueta: algunas opciones son para mamá y otras para el recién nacido.';
  const order=s.foods.map((_,i)=>i).sort((a,b)=>((a*7+state.stage*3)%s.foods.length)-((b*7+state.stage*3)%s.foods.length));
  $('foods').replaceChildren(...order.map(i=>{const f=s.foods[i],used=state.chosen.includes(`${state.stage}:${i}`),button=document.createElement('button');
    button.type='button';button.className='food'+(used?' chosen '+(f.good?'good':'bad'):'');button.disabled=used;button.draggable=!used;
    button.setAttribute('aria-label',`${f.name}. ${f.detail}. Para ${f.recipient}${used?'. Ya elegida':''}`);
    const icon=document.createElement('span');icon.className='emoji';icon.innerHTML=foodIcon(f.name);button.append(icon);
    for(const [tag,cls,text] of [['b','',f.name],['small','',f.detail],['span','recipient','Para '+f.recipient]]){const el=document.createElement(tag);el.className=cls;el.textContent=text;button.append(el);}
    if(used){const mark=document.createElement('span');mark.className='check';mark.textContent=f.good?'✓':'✕';button.append(mark);}
    button.onclick=()=>choose(i);button.ondragstart=e=>{e.dataTransfer.setData('text/plain',String(i));e.dataTransfer.effectAllowed='copy';};return button;}));
  $('next').disabled=!stats.ready;$('next').textContent=state.stage===4?'VER MI REPASO →':'SIGUIENTE ETAPA →';
  const remaining=stats.target-stats.stageGood;
  $('hint').textContent=stats.ready?'¡Etapa completada! Puedes seguir explorando o avanzar.':`Descubre ${remaining} ${remaining===1?'elección adecuada':'elecciones adecuadas'} más para avanzar.`;
  if(state.done)renderSummary(stats);resize();
}
function choose(index){
  if(paused)return;const before=state;state=E.choose(state,stages,index);if(before===state)return;
  const f=stages[state.stage].foods[index];save();render();
  $('feedback').className='feedback '+(f.good?'good':'bad');$('feedback').replaceChildren();
  const title=document.createElement('strong');title.textContent=(f.good?'✓ Buena elección: ':'✕ Revisemos esta elección: ')+f.name;
  $('feedback').append(title,document.createTextNode(f.explanation));
  clearTimeout(emotionTimer);$('dropzone').classList.remove('error','success');$('dropzone').classList.add(f.good?'success':'error');
  emotionTimer=setTimeout(()=>$('dropzone').classList.remove('error','success'),1800);
  Music.effect(f.good);speak((f.good?'Correcto. ':'Esta elección no es adecuada. ')+f.explanation);resize();
}
function renderSummary(stats){
  $('finalScore').textContent=`${stats.good} elecciones adecuadas · ${stats.errors} errores · 5 etapas recorridas`;
  $('finalRisk').textContent=E.risk(stats.errors)+'. Esta categoría mide aprendizaje, no riesgo clínico.';
  const mistakes=state.history.filter(h=>!h.good);$('review').replaceChildren();
  if(!mistakes.length){const p=document.createElement('p');p.textContent='¡Sin errores! Recuerda: alimentación variada y segura para mamá; leche materna o fórmula infantil apropiada para el recién nacido.';$('review').append(p);}
  for(const h of mistakes){const f=stages[h.stage].foods[h.index],d=document.createElement('details'),s=document.createElement('summary'),p=document.createElement('p');
    s.textContent=stages[h.stage].name+' · '+f.name;p.textContent=f.explanation;d.append(s,p);d.open=true;$('review').append(d);}
  const recap=document.createElement('details'),heading=document.createElement('summary');heading.textContent='Repasar las cinco etapas';recap.append(heading);
  for(const s of stages){const p=document.createElement('p');p.textContent=s.name+': '+s.lesson;recap.append(p);}$('review').append(recap);
}
$('start').onclick=async()=>{state.started=true;save();render();await Music.start();musicLabel();};
$('music').onclick=async()=>{await Music.toggle();musicLabel();};
$('pause').onclick=()=>{paused=true;$('board').inert=true;$('pausePanel').hidden=false;Music.stop();stopVoice();$('resume').focus();};
$('resume').onclick=async()=>{paused=false;$('board').inert=false;$('pausePanel').hidden=true;await Music.start();musicLabel();$('pause').focus();};
$('learn').onclick=()=>{const s=stages[state.stage];$('lessonTitle').textContent=s.name;$('lessonText').textContent=s.lesson;$('lesson').showModal();stopVoice();};
$('closeLesson').onclick=()=>$('lesson').close();
$('next').onclick=()=>{if(paused)return;const previous=state;state=E.next(state,stages);if(previous===state)return;stopVoice();save();
  $('feedback').className='feedback';$('feedback').textContent='Elige una tarjeta para descubrir su aporte o aprender por qué debes evitarla.';render();
  if(state.done){const stats=E.stats(state,stages);Music.stop();musicLabel();speak(`Completaste las cinco etapas con ${stats.good} aciertos y ${stats.errors} errores. Revisa tus elecciones en el resumen.`);}
  else{Music.effect(true);$('stageTitle').setAttribute('tabindex','-1');$('stageTitle').focus();}
};
$('restart').onclick=()=>{stopVoice();state={...E.fresh(),started:true};save();$('feedback').className='feedback';$('feedback').textContent='Comienza un nuevo recorrido y aplica lo aprendido.';render();Music.start().then(musicLabel);};
$('dropzone').ondragover=e=>{e.preventDefault();if(!paused)$('dropzone').classList.add('drop-ready');};
$('dropzone').ondragleave=()=>$('dropzone').classList.remove('drop-ready');
$('dropzone').ondrop=e=>{e.preventDefault();$('dropzone').classList.remove('drop-ready');const raw=e.dataTransfer.getData('text/plain');if(/^\d+$/.test(raw))choose(Number(raw));};
window.addEventListener('pagehide',stopVoice);
document.addEventListener('visibilitychange',()=>{if(document.hidden){stopVoice();if(state.started&&!state.done){paused=true;$('board').inert=true;$('pausePanel').hidden=false;}}});
window.addEventListener('message',event=>{
  if(event.source!==window.parent||event.data?.type!=='streamlit:render')return;
  const args=event.data.args;if(!Array.isArray(args.stages)||!args.session)return;
  stages=args.stages;if(session!==args.session){session=args.session;let saved=null;try{saved=sessionStorage.getItem('vida-game-'+session);}catch(_){}state=saved?E.restore(saved,stages):E.fresh();}
  $('sources').replaceChildren(...(args.sources||[]).map(([title,url])=>{const a=document.createElement('a');a.textContent=title;a.href=url;a.target='_blank';a.rel='noopener noreferrer';return a;}));
  render();musicLabel();
});
post('streamlit:componentReady',{apiVersion:1});resize();
