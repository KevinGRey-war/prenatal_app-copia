'use strict';
const $=id=>document.getElementById(id), E=GameEngine;
let stages=[],state=E.fresh(),session='',paused=false,emotionTimer,lastHeight=0,voiceGeneration=0;
let artworkReady=false,lastPublished='';
const artworkUrls=[];
function loadArtwork(artwork){
  if(artworkReady||!artwork?.characters||!artwork?.foods)return;
  const makeUrl=data=>{
    const raw=atob(data),bytes=Uint8Array.from(raw,c=>c.charCodeAt(0));
    const url=URL.createObjectURL(new Blob([bytes],{type:'image/png'}));
    artworkUrls.push(url);return url;
  };
  $('game').style.setProperty('--character-art',`url("${makeUrl(artwork.characters)}")`);
  setFoodArtwork(makeUrl(artwork.foods));artworkReady=true;
}
function post(type,extra={}){window.parent.postMessage({isStreamlitMessage:true,type,...extra},'*');}
function publishFinal(){
  if(!state.done)return;
  const value={history:state.history.map(h=>({stage:h.stage,index:h.index}))};
  const signature=session+JSON.stringify(value);
  if(signature===lastPublished)return;
  lastPublished=signature;
  post('streamlit:setComponentValue',{value,dataType:'json'});
}
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
  return `<span class="character stage-${stage}" aria-hidden="true"></span>`;
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
  $('recipientHint').textContent='Arrastra o toca las acciones para acompañar a mamá. Los puntos representan aprendizaje.';
  $('eventTitle').textContent=s.emergency.title;
  $('eventSituation').textContent=s.emergency.situation;
  const order=s.foods.map((_,i)=>i).sort((a,b)=>((a*7+state.stage*3)%9)-((b*7+state.stage*3)%9));
  $('foods').replaceChildren(...order.map(i=>{const f=s.foods[i],used=state.chosen.includes(`${state.stage}:${i}`),button=document.createElement('button');
    button.type='button';button.className='food'+(used?' chosen '+(f.good?'good':'bad'):'');button.disabled=used;button.draggable=!used;
    button.setAttribute('aria-label',`${f.name}. ${f.detail}. Para ${f.recipient}${used?'. Ya elegida':''}`);
    const icon=document.createElement('span');icon.className='emoji';icon.innerHTML=careIcon(f.icon);button.append(icon);
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
  $('finalScore').textContent=`${stats.good} elecciones adecuadas · ${stats.errors} ${stats.errors===1?'error':'errores'} · 5 etapas recorridas`;
  $('finalRisk').textContent=E.risk(stats.errors)+'. Esta categoría mide aprendizaje, no riesgo clínico.';
  const mistakes=state.history.filter(h=>!h.good);$('review').replaceChildren();
  if(!mistakes.length){const p=document.createElement('p');p.textContent='¡Sin errores! Practicaste acciones de cuidado y búsqueda oportuna de ayuda. Los alimentos no sustituyen la atención de una emergencia.';$('review').append(p);}
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
  $('feedback').className='feedback';$('feedback').textContent='Elige una acción para acompañar a mamá y aprender a actuar ante este evento.';render();
  if(state.done){const stats=E.stats(state,stages);Music.stop();musicLabel();
    publishFinal();
    const review=state.history.filter(h=>!h.good).map(h=>{const f=stages[h.stage].foods[h.index];return stages[h.stage].name+'. '+f.name+'. '+f.explanation;}).join(' ');
    speak(`¡Felicitaciones por completar tu aprendizaje! Practicaste cómo reconocer señales de alarma y pedir ayuda. Completaste las cinco etapas con ${stats.good} aciertos y ${stats.errors} errores. ${E.risk(stats.errors)}. Esta categoría mide aprendizaje, no la salud de mamá ni del bebé. `+(review||'Todas tus elecciones fueron adecuadas. Recuerda lo aprendido en cada etapa.'));}

  else{$('dropzone').classList.remove('error','success');const scene=document.querySelector('.scene-layout');scene.classList.remove('entering');void scene.offsetWidth;scene.classList.add('entering');Music.effect(true);$('stageTitle').setAttribute('tabindex','-1');$('stageTitle').focus();}
};
$('restart').onclick=()=>{stopVoice();lastPublished='';state={...E.fresh(),started:true};save();post('streamlit:setComponentValue',{value:null,dataType:'json'});$('feedback').className='feedback';$('feedback').textContent='Comienza un nuevo recorrido y aplica lo aprendido.';render();Music.start().then(musicLabel);};
$('dropzone').ondragover=e=>{e.preventDefault();if(!paused)$('dropzone').classList.add('drop-ready');};
$('dropzone').ondragleave=()=>$('dropzone').classList.remove('drop-ready');
$('dropzone').ondrop=e=>{e.preventDefault();$('dropzone').classList.remove('drop-ready');const raw=e.dataTransfer.getData('text/plain');if(/^\d+$/.test(raw))choose(Number(raw));};
window.addEventListener('pagehide',stopVoice);
window.addEventListener('pagehide',()=>artworkUrls.forEach(url=>URL.revokeObjectURL(url)));
document.addEventListener('visibilitychange',()=>{if(document.hidden){stopVoice();if(state.started&&!state.done){paused=true;$('board').inert=true;$('pausePanel').hidden=false;}}});
window.addEventListener('message',event=>{
  if(event.source!==window.parent||event.data?.type!=='streamlit:render')return;
  const args=event.data.args;if(!Array.isArray(args.stages)||!args.session)return;
  loadArtwork(args.artwork);
  stages=args.stages;if(session!==args.session){session=args.session;let saved=null;try{saved=sessionStorage.getItem('vida-game-'+session);}catch(_){}state=saved?E.restore(saved,stages):E.fresh();}
  $('sources').replaceChildren(...(args.sources||[]).map(([title,url])=>{const a=document.createElement('a');a.textContent=title;a.href=url;a.target='_blank';a.rel='noopener noreferrer';return a;}));
  render();musicLabel();publishFinal();
});
post('streamlit:componentReady',{apiVersion:1});resize();
