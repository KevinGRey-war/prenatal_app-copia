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
  return `<svg viewBox="0 0 300 300" aria-hidden="true">${defs}
  <ellipse cx="150" cy="275" rx="95" ry="15" fill="#59963730"/>
  <g stroke="#895032" stroke-width="3" stroke-linejoin="round">
  <ellipse class="skin" cx="87" cy="249" rx="36" ry="24" fill="url(#skin)" transform="rotate(-25 87 249)"/>
  <ellipse class="skin" cx="212" cy="249" rx="36" ry="24" fill="url(#skin)" transform="rotate(25 212 249)"/>
  <path d="M111 165Q91 204 108 250Q150 273 194 248Q211 204 188 165Z" fill="#40b9ec"/>
  <path d="M123 167V212Q150 232 178 212V167" fill="#fff6d6"/>
  <path d="M150 209v-19m0 7q-22 0-19-15q19 0 19 15m0-4q1-17 18-15q-1 16-18 15" fill="#88c944" stroke="#4b9236" stroke-width="2"/>
  <path class="skin" d="M112 181Q89 171 73 151Q54 142 47 158Q51 187 98 211" fill="url(#skin)"/>
  <path class="skin" d="M187 179Q212 168 223 145Q242 134 250 151Q245 184 202 207" fill="url(#skin)"/>
  <circle class="skin" cx="79" cy="112" r="18" fill="url(#skin)"/><circle class="skin" cx="222" cy="112" r="18" fill="url(#skin)"/>
  <path class="skin" d="M79 103Q72 36 149 31Q225 32 223 108Q232 168 152 181Q78 173 79 103Z" fill="url(#skin)"/>
  <path d="M80 99Q54 54 101 30Q132 5 174 26Q211 19 227 67L220 104Q207 65 191 64Q201 85 168 75Q182 53 156 51Q114 85 106 63Q108 86 80 99Z" fill="#9b562b"/>
  <path d="M92 55Q116 29 150 31M169 35q26-6 41 20" fill="none" stroke="#df9a4e" stroke-width="6" stroke-linecap="round"/>
  <ellipse cx="119" cy="111" rx="15" ry="21" fill="#fff" stroke="none"/><ellipse cx="181" cy="111" rx="15" ry="21" fill="#fff" stroke="none"/>
  <ellipse cx="122" cy="114" rx="10" ry="16" fill="#593522"/><ellipse cx="178" cy="114" rx="10" ry="16" fill="#593522"/>
  <g fill="white" stroke="none"><circle cx="125" cy="107" r="5"/><circle cx="181" cy="107" r="5"/></g>
  <g fill="#f79582" stroke="none" opacity=".65"><ellipse cx="100" cy="137" rx="17" ry="10"/><ellipse cx="202" cy="137" rx="17" ry="10"/></g>
  <path d="M145 131q5 5 10 0" fill="none" stroke="#d58b65" stroke-linecap="round"/>
  <path class="happy-mouth" d="M131 144Q150 151 172 142Q166 171 150 167Q136 166 131 144Z" fill="#9b3b33"/>
  <path class="sad-mouth" d="M131 158Q148 126 171 156Q151 150 131 158Z" fill="#9b3b33"/>
  <path class="tear" d="M106 127q-13 23 0 23q13 0 0-23M195 127q-13 23 0 23q13 0 0-23" fill="#57c9f7" stroke="#fff" stroke-width="2"/>
  </g></svg>`;
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
  $('reaction').textContent=f.good?'¡Muy bien! ★':'¡Vamos a aprender!';
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
  else{$('dropzone').classList.remove('error','success');const scene=document.querySelector('.scene-layout');scene.classList.remove('entering');void scene.offsetWidth;scene.classList.add('entering');Music.effect(true);$('stageTitle').setAttribute('tabindex','-1');$('stageTitle').focus();}
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
