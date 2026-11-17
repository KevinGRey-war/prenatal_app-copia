/* Pure state transitions shared by the browser and Node regression tests. */
(function(root){
  const fresh=()=>({stage:0,chosen:[],history:[],done:false,started:false});
  function risk(errors){return errors>=11?'Riesgo educativo alto':errors>=5?'Riesgo educativo leve':'Sin riesgo educativo';}
  function stats(state,stages){
    const entries=state.history,good=entries.filter(e=>e.good).length;
    const stageGood=entries.filter(e=>e.stage===state.stage&&e.good).length;
    const target=stages[state.stage].foods.filter(f=>f.good).length;
    return {good,errors:entries.length-good,stageGood,target,ready:stageGood===target,
      total:stages.reduce((sum,s)=>sum+s.foods.filter(f=>f.good).length,0)};
  }
  function choose(state,stages,index){
    if(!state.started||state.done||!Number.isInteger(index))return state;
    const food=stages[state.stage].foods[index],key=`${state.stage}:${index}`;
    if(!food||state.chosen.includes(key))return state;
    return {...state,chosen:[...state.chosen,key],history:[...state.history,{stage:state.stage,index,good:food.good}]};
  }
  function next(state,stages){
    if(!stats(state,stages).ready||state.done)return state;
    return state.stage===stages.length-1?{...state,done:true}:{...state,stage:state.stage+1};
  }
  function restore(raw,stages){
    try{
      const saved=JSON.parse(raw);if(!Array.isArray(saved.history))return fresh();
      let state={...fresh(),started:!!saved.started};
      for(const e of saved.history){
        while(e.stage>state.stage&&stats(state,stages).ready&&state.stage<stages.length-1)state=next(state,stages);
        if(e.stage!==state.stage)return fresh();
        state=choose(state,stages,e.index);
      }
      if(saved.stage===state.stage+1)state=next(state,stages);
      if(saved.done)state=next(state,stages);
      return state;
    }catch(_){return fresh();}
  }
  const api={fresh,risk,stats,choose,next,restore};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.GameEngine=api;
})(typeof window!=='undefined'?window:globalThis);
