const assert=require('node:assert/strict');
const E=require('../gestation_game/engine.js');
const stages=JSON.parse(require('node:fs').readFileSync(0,'utf8'));
const {foodIcon}=require('../gestation_game/icons.js');
for(const stage of stages)for(const food of stage.foods){const icon=foodIcon(food.name);assert(icon.includes('<svg'));assert(!icon.includes('<script'));}
let state=E.fresh();
assert.equal(E.choose(state,stages,0),state,'Must start before choosing');
state.started=true;
assert.equal(E.next(state,stages),state,'Cannot skip an unfinished stage');
assert.equal(E.choose(state,stages,-1),state);
for(let stage=0;stage<5;stage++){
  assert.equal(state.stage,stage);
  for(let i=0;i<stages[stage].foods.length;i++){
    state=E.choose(state,stages,i);
    assert.equal(E.choose(state,stages,i),state,'Duplicate choice cannot change score');
    assert.deepEqual(E.restore(JSON.stringify(state),stages),state,'Progress must restore');
  }
  assert.equal(E.stats(state,stages).ready,true);
  state=E.next(state,stages);
  assert.deepEqual(E.restore(JSON.stringify(state),stages),state,'Stage transition must restore');
}
assert.equal(state.done,true);
assert.equal(E.stats(state,stages).good,25);
assert.equal(E.stats(state,stages).errors,20);
assert.equal(E.choose(state,stages,0),state,'Finished games cannot score');
for(const [n,label]of [[0,'Sin'],[4,'Sin'],[5,'leve'],[10,'leve'],[11,'alto'],[20,'alto']])assert(E.risk(n).includes(label));
assert.deepEqual(E.restore('{bad json',stages),E.fresh());
assert.deepEqual(E.restore(JSON.stringify({history:[{stage:4,index:0}],started:true}),stages),E.fresh());
let perfect={...E.fresh(),started:true};
for(const stage of stages){stage.foods.forEach((f,i)=>{if(f.good)perfect=E.choose(perfect,stages,i);});perfect=E.next(perfect,stages);}
assert.equal(perfect.done,true);assert.equal(E.stats(perfect,stages).errors,0);
console.log('Game transitions, all five stages, duplicate prevention, persistence and risk boundaries passed.');
