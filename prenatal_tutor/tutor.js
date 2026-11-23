'use strict';
const $=id=>document.getElementById(id);
let token='',cards=[],index=0,generation=0,active=null,busy=false,complete=false;
function post(type,extra={}){parent.postMessage({isStreamlitMessage:true,type,...extra},'*');}
function resize(){post('streamlit:setFrameHeight',{height:Math.ceil(document.querySelector('.panel').getBoundingClientRect().height)+4});}
new ResizeObserver(resize).observe(document.querySelector('.panel'));
function stop(){generation++;if(active instanceof Audio){active.pause();active.src='';}if('speechSynthesis'in window)speechSynthesis.cancel();busy=false;$('avatar').classList.remove('talking');}
function blocked(){$('retry').hidden=false;busy=false;$('avatar').classList.remove('talking');$('status').textContent='La voz no pudo continuar. Activa la explicación de voz para reintentar. El avance permanece bloqueado.';resize();}
function play(){
  if(busy||complete||!cards.length)return;
  stop();$('retry').hidden=true;busy=true;const own=generation,card=cards[index];
  $('title').textContent=card.title;$('text').textContent=card.text;
  $('progress').max=cards.length;$('progress').value=index;
  $('status').textContent=`Escucha el repaso ${index+1} de ${cards.length}. Podrás continuar cuando termine.`;
  const started=()=>{if(own===generation)$('avatar').classList.add('talking');};
  const ended=()=>{if(own!==generation)return;busy=false;$('avatar').classList.remove('talking');index++;$('progress').value=index;
    if(index===cards.length){complete=true;$('status').textContent='Retroalimentación terminada. Ya puedes continuar.';post('streamlit:setComponentValue',{value:{token,completed:index},dataType:'json'});resize();}else play();};
  function spoken(){
    if(!('speechSynthesis'in window)){blocked();return;}
    const words=card.text.split(/\s+/),parts=[];let line='';
    for(const word of words){if(line.length+word.length>160){parts.push(line);line='';}line+=(line?' ':'')+word;}if(line)parts.push(line);
    let part=0;
    function next(){if(own!==generation)return;if(part===parts.length){ended();return;}
      active=new SpeechSynthesisUtterance(parts[part++]);active.lang='es-ES';active.rate=.96;
      const voice=speechSynthesis.getVoices().find(v=>v.lang.startsWith('es'));if(voice)active.voice=voice;
      active.onstart=started;active.onresume=started;active.onpause=()=>{if(own===generation)$('avatar').classList.remove('talking');};
      active.onend=()=>{if(own===generation)$('avatar').classList.remove('talking');next();};active.onerror=()=>{if(own===generation)blocked();};speechSynthesis.speak(active);
    }next();
  }
  if(card.audio){active=new Audio('data:audio/mpeg;base64,'+card.audio);active.onplaying=started;active.onpause=active.onwaiting=()=>{if(own===generation)$('avatar').classList.remove('talking');};active.onended=ended;active.onerror=()=>{if(own===generation)spoken();};active.play().catch(()=>{if(own===generation)spoken();});}else spoken();resize();
}
$('avatar').onclick=()=>{if(!busy)play();};
$('retry').onclick=()=>{if(!busy)play();};
window.addEventListener('message',event=>{if(event.source!==parent||event.data?.type!=='streamlit:render')return;
  const args=event.data.args;if(!args.token||!Array.isArray(args.cards)||!args.cards.length||args.token===token)return;
  document.querySelector('.panel').classList.toggle('compact',Boolean(args.compact));
  stop();token=args.token;cards=args.cards;index=0;complete=false;play();
});
window.addEventListener('pagehide',stop);
post('streamlit:componentReady',{apiVersion:1});resize();
