/* Original composition: Jardín de vida. Synthesized locally; no downloads. */
const Music = (() => {
  let ctx, timer, playing=false, step=0, volume=.12, ducked=false;
  const melody=[72,76,79,83,81,79,76,0,74,77,81,84,83,79,77,0,
                76,79,84,88,86,84,79,0,74,77,81,79,76,74,72,0];
  const roots=[48,53,57,55];
  function context(){ctx ||= new (window.AudioContext||window.webkitAudioContext)();return ctx;}
  function note(midi, length=.5, delay=0, level=.2){
    if(!ctx||ctx.state!=='running')return;
    const osc=ctx.createOscillator(),gain=ctx.createGain(),t=ctx.currentTime+delay;
    osc.type='sine';osc.frequency.value=440*Math.pow(2,(midi-69)/12);
    gain.gain.setValueAtTime(0,t);gain.gain.linearRampToValueAtTime(level*volume*(ducked?.2:1),t+.025);
    gain.gain.exponentialRampToValueAtTime(.0001,t+length);
    osc.connect(gain);gain.connect(ctx.destination);osc.start(t);osc.stop(t+length+.03);
  }
  function tick(){
    if(!playing||document.hidden)return;
    const n=melody[step%melody.length];if(n)note(n,.9,0,.25);
    if(step%4===0){const root=roots[Math.floor(step/8)%4];note(root,2,0,.16);note(root+7,1.6,.14,.10);}
    step++;
  }
  async function start(){
    try{
      if(sessionStorage.getItem('vida-music')==='off')return;
      const c=context();
      // Do not wait forever on a browser that requires a direct user gesture.
      if(c.state==='suspended')c.resume().catch(()=>{});
      if(c.state!=='running'){await new Promise(r=>setTimeout(r,70));}
      if(c.state!=='running')return;
      if(timer)clearInterval(timer);playing=true;tick();timer=setInterval(tick,470);
    }catch(_){playing=false;}
  }
  function stop(){playing=false;clearInterval(timer);timer=null;}
  async function toggle(){if(playing){stop();sessionStorage.setItem('vida-music','off');}
    else{sessionStorage.setItem('vida-music','on');await start();}}
  async function effect(good){try{await context().resume();
    if(good){note(76,.22,0,.5);note(79,.24,.12,.4);note(84,.35,.24,.35);}
    else{note(57,.25,0,.35);note(53,.35,.16,.3);}
  }catch(_){}}
  function duck(value){ducked=value;}
  window.addEventListener('pagehide',()=>{stop();if(ctx)ctx.close();});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  return {start,stop,toggle,effect,duck,get playing(){return playing;}};
})();
