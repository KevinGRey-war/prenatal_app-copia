/* Original vector pictograms. Same rounded lines and palette on every device. */
(function(root){
  const wrap=shape=>`<svg viewBox="0 0 80 80" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg"><ellipse cx="40" cy="69" rx="25" ry="5" fill="#74546b12"/><g stroke="#785d70" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${shape}</g></svg>`;
  const leaf='<path d="M40 20Q45 8 58 14Q55 25 40 20Z" fill="#98bea0"/><path d="M39 25l3-12" fill="none"/>';
  const shapes={
    apple:leaf+'<path d="M40 27C15 10 12 39 22 57Q32 72 40 65Q50 73 59 57C71 36 61 11 40 27Z" fill="#ec9cad"/><path d="M25 32q-5 8-2 15" stroke="#ffdee5" stroke-width="5"/>',
    orange:leaf+'<circle cx="40" cy="45" r="23" fill="#f4bb75"/><path d="M24 37q2-7 9-9" stroke="#ffe1ab" stroke-width="5"/><circle cx="54" cy="48" r="1" fill="#dc985e" stroke="none"/><circle cx="49" cy="56" r="1" fill="#dc985e" stroke="none"/>',
    pear:leaf+'<path d="M31 27q9-12 18 0c0 16 17 17 17 31q-1 16-26 13Q13 73 14 56c0-12 17-15 17-29Z" fill="#c4d29b"/><path d="M27 49q-7 8-3 12" stroke="#e7ebc3" stroke-width="4"/>',
    avocado:'<path d="M29 18q11-15 22 0l16 32q7 22-27 22Q8 73 13 51Z" fill="#91b897"/><path d="M32 23q8-10 16 0l13 28q5 16-21 16Q15 68 19 52Z" fill="#dde1a5"/><circle cx="40" cy="50" r="12" fill="#b28766"/>',
    banana:'<path d="M60 13Q61 60 13 49Q22 75 49 63Q74 54 67 19Z" fill="#f2d387"/><path d="M24 57q32 8 39-30" fill="none" stroke="#d7af5d"/><path d="M60 13l3-5 6 2-2 9Z" fill="#a4b77c"/>',
    beans:'<path d="M24 16C7 24 10 52 27 48Q41 44 31 34Q25 29 33 22Q33 14 24 16Z" fill="#d6a19b"/><path d="M52 32C34 39 37 68 54 64Q68 60 58 50Q52 45 61 38Q62 30 52 32Z" fill="#ba8b9d"/><path d="M19 26q-5 10 1 14m27 2q-6 10 1 14" fill="none" stroke="#f7dfd2"/>',
    greens:'<path d="M39 68Q2 43 15 24Q22 12 35 29Q43 2 58 18Q78 42 39 68Z" fill="#97c2a1"/><path d="M39 68l4-37m-4 21-16-16m18 7 15-14" fill="none" stroke="#5d9279"/>',
    broccoli:'<path d="M31 41l-2 28h23l-4-28Z" fill="#bccea0"/><path d="M20 47C2 43 10 22 24 26C22 8 49 5 52 24C70 13 79 43 61 48Z" fill="#8cb397"/><path d="M27 49l11 9m14-12L40 61" fill="none"/>',
    carrot:'<path d="M31 30Q50 20 60 34L25 70Q14 77 18 63Z" fill="#edb18a"/><path d="M45 27l-2-15m8 14 9-17m-2 21 12-6" fill="none" stroke="#86ae8c" stroke-width="5"/><path d="M28 43l9 5m-15 6 7 4" fill="none"/>',
    pumpkin:'<path d="M37 24q-4-9 4-14l5 3-3 11" fill="#a9bc8e"/><ellipse cx="40" cy="45" rx="29" ry="23" fill="#eab28b"/><ellipse cx="40" cy="45" rx="17" ry="23" fill="#f5c297"/><path d="M40 22v46" fill="none" stroke="#d59a7c"/>',
    potato:'<path d="M23 27C42 5 72 27 66 49C62 72 23 77 14 57Q3 38 23 27Z" fill="#d5bb9d"/><path d="M27 33l3 2m18-5 2 3m-24 20 3 2m24-8 2 3" stroke="#aa8f79"/>',
    grain:'<path d="M14 44h52Q61 69 40 69Q19 68 14 44Z" fill="#c8b6d9"/><ellipse cx="40" cy="44" rx="26" ry="7" fill="#fff2d4"/><path d="M42 38V10m-2 19q-14-2-12-11 12 0 12 11m4-8q12-2 11-10-11 1-11 10m-4 19q-14-2-12-11 12 0 12 11" fill="#dec795"/>',
    egg:'<path d="M40 12C23 12 9 48 20 62Q40 80 60 62C72 48 57 12 40 12Z" fill="#fff1da"/><path d="M28 27q-9 12-8 22" fill="none" stroke="#fff" stroke-width="5"/>',
    fish:'<path d="M60 37l14-13v33L60 45Q34 73 10 41Q35 8 60 37Z" fill="#9ec5cf"/><path d="M30 25q12 15 0 31" fill="none"/><circle cx="23" cy="37" r="3" fill="#5d6475" stroke="none"/><path d="M42 29l8-9 5 11m-12 21 8 9 3-12" fill="#b0d8d6"/>',
    chicken:'<path d="M24 51l-9 10q-9-4-9 3 0 8 8 5 2 9 9 4 6-5 1-10l12-11Z" fill="#fff4df"/><path d="M27 52C6 33 36 7 58 17C83 29 62 60 43 57Z" fill="#dba88a"/><path d="M36 25q14-8 21 1" fill="none" stroke="#f7ceb0" stroke-width="5"/>',
    cheese:'<path d="M12 37l42-19 14 19v29H12Z" fill="#efce88"/><path d="M12 37h56" fill="none"/><circle cx="26" cy="50" r="4" fill="#ddb878"/><circle cx="52" cy="57" r="5" fill="#ddb878"/>',
    milk:'<path d="M27 12h26l10 14v43H17V26Z" fill="#fff9ee"/><path d="M17 26h46v17H17Z" fill="#b5d4d1"/><path d="M27 12v14m26-14v14" fill="none"/><path d="M40 46q-15 17 0 19 15-2 0-19" fill="#b5d4d1"/>',
    yogurt:'<path d="M20 27h40l-5 42H25Z" fill="#fff4ed"/><path d="M22 39h36l-2 18H24Z" fill="#d3badf"/><ellipse cx="40" cy="27" rx="23" ry="6" fill="#eddbe7"/><path d="M50 19l10-12" fill="none" stroke-width="4"/>',
    bottle:'<path d="M31 22v-6q0-9 9-9t9 9v6" fill="#ebc2aa"/><path d="M24 25h32v9l6 9v25H18V43l6-9Z" fill="#fdf8ed"/><path d="M24 24h32v10H24Z" fill="#c3acdd"/><path d="M20 50h40v16H20Z" fill="#f1e1c4"/><path d="M47 42h8m-8 6h8" fill="none"/>',
    water:'<path d="M40 8C32 27 11 37 15 53Q21 78 46 69C75 61 65 39 40 8Z" fill="#acd5df"/><path d="M25 43q-5 12 6 17" fill="none" stroke="#e7fbff" stroke-width="5"/>',
    bowl:'<path d="M10 40h60Q64 68 40 68Q15 67 10 40Z" fill="#b6d4c8"/><ellipse cx="40" cy="40" rx="30" ry="8" fill="#f2d9a6"/><path d="M26 27q-8-7 0-14m14 12q-8-7 0-14m14 16q-8-7 0-14" fill="none" stroke="#bfb1c6"/><circle cx="28" cy="40" r="3" fill="#c2b480"/><circle cx="46" cy="42" r="4" fill="#d8997c"/>',
    nuts:'<path d="M25 20C8 25 7 63 23 68C42 73 42 36 25 20Z" fill="#c49b81"/><path d="M50 17C33 22 31 59 47 64C65 69 68 34 50 17Z" fill="#d2ad88"/><path d="M23 31v26m25-29v26" fill="none" stroke="#eed4b5"/>',
    honey:'<path d="M23 23h34v11l6 7v27H17V41l6-7Z" fill="#ebc481"/><path d="M21 18h38v9H21Z" fill="#c3a0bf"/><rect x="23" y="42" width="34" height="18" rx="6" fill="#fff4d3"/><path d="M40 45q-8 8 0 11 8-3 0-11Z" fill="#d9a665"/>',
    cup:'<path d="M17 28h39v25q0 15-20 15T17 53Z" fill="#ebd4e8"/><path d="M56 34q24 0 10 19H56" fill="none"/><ellipse cx="36" cy="28" rx="19" ry="5" fill="#c5ba98"/><path d="M28 17q-6-7 0-12m17 12q-6-7 0-12" fill="none" stroke="#bfb0c8"/>',
    wine:'<path d="M23 12h34v21q0 17-17 17T23 33Z" fill="#f2e2ec"/><path d="M25 29h30v6q-2 13-15 13T25 35Z" fill="#cb95ad"/><path d="M40 50v18m-13 1h26" fill="none"/>',
    soda:'<path d="M22 23h36l-5 47H27Z" fill="#dca8c0"/><path d="M19 23h42" stroke-width="5"/><path d="M40 44l6-32 11-6" fill="none" stroke="#a3bdb7" stroke-width="4"/><path d="M24 38h31l-2 17H26" fill="#f6e2ec"/>',
    meat:'<path d="M20 21C43 7 71 30 66 52Q65 73 42 66Q18 76 11 53C3 37 7 28 20 21Z" fill="#d5a0a3"/><path d="M24 29q22-11 30 17q3 17-17 10q-18 8-17-11" fill="none" stroke="#f6ded6" stroke-width="7"/>',
    sushi:'<ellipse cx="40" cy="30" rx="26" ry="14" fill="#a7b9a0"/><path d="M14 30v27q26 20 52 0V30" fill="#8fa598"/><ellipse cx="40" cy="30" rx="22" ry="11" fill="#fff2dc"/><ellipse cx="40" cy="30" rx="11" ry="7" fill="#e8aa98"/>',
    warning:'<circle cx="40" cy="40" r="28" fill="#f4dbe4"/><path d="M40 23v22m0 10v2" stroke="#b77391" stroke-width="6"/>',
    breast:'<path d="M14 67q3-34 27-38 26 6 27 38" fill="#c7a8dc"/><circle cx="40" cy="18" r="12" fill="#f2ceb0"/><path d="M22 45q20 29 40-1" fill="none" stroke="#efc6a8" stroke-width="11"/><circle cx="48" cy="45" r="11" fill="#f5d2b0"/><path d="M31 48l17 12" stroke="#fff4f7" stroke-width="9"/>',
  };
  function foodIcon(name){
    const n=name.toLowerCase();let key='bowl';
    if(/leche materna/.test(n))key='breast';else if(/fórmula/.test(n))key='bottle';
    else if(/agua o infusiones|infusión/.test(n))key='cup';else if(/agua potable/.test(n))key='water';
    else if(/leche/.test(n))key='milk';else if(/yogur/.test(n))key='yogurt';else if(/queso/.test(n))key='cheese';
    else if(/lenteja|fréjol|garbanzo/.test(n))key='beans';else if(/espinaca|brotes|ensalada/.test(n))key='greens';
    else if(/brócoli/.test(n))key='broccoli';else if(/naranja/.test(n))key='orange';else if(/aguacate/.test(n))key='avocado';
    else if(/avena|quinua|arroz/.test(n))key='grain';else if(/huevo/.test(n))key='egg';else if(/pollo/.test(n))key='chicken';
    else if(/salmón|pez/.test(n))key='fish';else if(/sushi/.test(n))key='sushi';else if(/carne/.test(n))key='meat';
    else if(/zanahoria/.test(n))key='carrot';else if(/pera/.test(n))key='pear';else if(/nueces/.test(n))key='nuts';
    else if(/papa/.test(n)&&!/papilla/.test(n))key='potato';else if(/banana/.test(n))key='banana';else if(/calabaza/.test(n))key='pumpkin';
    else if(/alcohol/.test(n))key='wine';else if(/gaseosa|energética/.test(n))key='soda';else if(/miel/.test(n))key='honey';
    else if(/ayunar|ayuno/.test(n))key='warning';else if(/fruta/.test(n)&&!/papilla/.test(n))key='apple';
    return wrap(shapes[key]);
  }
  if(typeof module!=='undefined'&&module.exports)module.exports={foodIcon};else root.foodIcon=foodIcon;
})(typeof window!=='undefined'?window:globalThis);
