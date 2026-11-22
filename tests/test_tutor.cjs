const {strict:assert}=require('assert'),vm=require('vm'),fs=require('fs');
const nodes={},messages=[],listeners={},utterances=[];
const node=id=>nodes[id]??={textContent:'',classList:{add(){},remove(){}}};
const parent={postMessage:m=>messages.push(m)};
const context={parent,document:{getElementById:node,querySelector:()=>node('panel'),documentElement:{scrollHeight:500}},
  window:{parent,addEventListener:(type,fn)=>listeners[type]=fn},Audio:class{},SpeechSynthesisUtterance:class{constructor(text){this.text=text;}},
  ResizeObserver:class{observe(){}},speechSynthesis:{cancel(){},getVoices:()=>[],speak:u=>utterances.push(u)}};
context.window.speechSynthesis=context.speechSynthesis;
vm.createContext(context);vm.runInContext(fs.readFileSync('prenatal_tutor/tutor.js','utf8'),context);
const render=()=>listeners.message({source:parent,data:{type:'streamlit:render',args:{token:'attempt',cards:[{title:'Uno',text:'Primera explicación.'},{title:'Dos',text:'Segunda explicación.'}]}}});
const completed=()=>messages.filter(m=>m.type==='streamlit:setComponentValue');
render();assert.equal(nodes.title.textContent,'Uno');assert.equal(completed().length,0);
utterances.at(-1).onerror();assert.equal(completed().length,0);assert.match(nodes.status.textContent,/bloqueado/);
nodes.avatar.onclick();utterances.at(-1).onend();assert.equal(nodes.title.textContent,'Dos');assert.equal(completed().length,0);
render();assert.equal(nodes.title.textContent,'Dos');
utterances.at(-1).onend();assert.equal(completed().length,1);assert.equal(completed()[0].value.completed,2);
render();assert.equal(completed().length,1);console.log('Tutor: sequential narration, error retry and completion gating passed');
