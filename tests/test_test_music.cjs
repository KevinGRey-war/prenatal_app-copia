const {strict:assert}=require('assert'),vm=require('vm'),fs=require('fs');
const html=fs.readFileSync('test_music/index.html','utf8'),script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes={},events={},prefs=new Map(),music={playing:false,starts:0,stops:0,async start(){this.playing=true;this.starts++;},stop(){this.playing=false;this.stops++;}};
const parent={postMessage(){}},window={fakeMusic:music,addEventListener:(key,fn)=>events[key]=fn};
const context={parent,window,sessionStorage:{getItem:k=>prefs.get(k)??null,setItem:(k,v)=>prefs.set(k,v)},document:{getElementById:id=>nodes[id]??={setAttribute(){}},createElement:()=>({}),head:{append(script){vm.runInContext(script.textContent,context);}}}};
vm.createContext(context);vm.runInContext(script,context);
const render=narrating=>events.message({source:parent,data:{type:'streamlit:render',args:{music:'const Music=window.fakeMusic;',narrating}}});
(async()=>{
 await render(false);assert.equal(music.playing,true);
 await render(true);assert.equal(music.playing,false);assert.match(nodes.status.textContent,/pausa/);
 await render(false);assert.equal(music.playing,true);
 await nodes.toggle.onclick();assert.equal(music.playing,false);
 await render(true);await render(false);assert.equal(music.playing,false,'Mute survives question changes');
 await nodes.toggle.onclick();assert.equal(music.playing,true);
 assert.equal(prefs.has('vida-music'),false,'Quiz does not change game music preference');
 console.log('Quiz music: starts, pauses for narration, resumes and preserves mute preference');
})().catch(error=>{console.error(error);process.exitCode=1;});
