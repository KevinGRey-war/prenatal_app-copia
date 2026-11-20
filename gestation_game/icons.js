/* Painted atlas icons, kept inside native SVG viewports for crisp sizing. */
(function(root){
  let atlasUrl='assets/foods-v2.png';
  root.setFoodArtwork=url=>{atlasUrl=url;};
  const keys=['apple','orange','pear','avocado','banana','beans','greens','broccoli','carrot','pumpkin','potato','grain','egg','fish','chicken','cheese','milk','yogurt','bottle','water','bowl','nuts','honey','cup','wine','soda','meat','sushi','warning','breast'];
  function foodIcon(name){
    const n=name.toLowerCase();let key='bowl';
    if(/huevo crudo/.test(n))return '<svg viewBox="0 0 80 80" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="rawEgg" cx="35%" cy="30%"><stop stop-color="#fffdf4"/><stop offset=".7" stop-color="#f2ddbd"/><stop offset="1" stop-color="#cfae88"/></radialGradient></defs><ellipse cx="40" cy="71" rx="23" ry="4" fill="#68493818"/><path d="M40 8C23 8 8 44 16 60C25 78 55 78 64 60C72 44 57 8 40 8Z" fill="url(#rawEgg)" stroke="#b69a7e" stroke-width="1.3"/></svg>';
    if(/papilla de frutas/.test(n))key='apple';else
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
    const index=keys.indexOf(key),x=(index%5)*200,y=Math.floor(index/5)*200;
    return `<svg viewBox="${x} ${y} 200 200" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg"><image href="${atlasUrl}" width="1000" height="1200" preserveAspectRatio="none"/></svg>`;
  }
  if(typeof module!=='undefined'&&module.exports)module.exports={foodIcon};else root.foodIcon=foodIcon;
})(typeof window!=='undefined'?window:globalThis);

/* Cohesive care-action icons, independent from the food illustration atlas. */
(function(root){
  const drawings={
    care:'<rect x="18" y="24" width="44" height="36" rx="9" fill="#fff7fb"/><path d="M29 24v-7h22v7M40 34v17M32 42h16"/>',
    support:'<circle cx="29" cy="28" r="9"/><circle cx="52" cy="31" r="8"/><path d="M13 59v-7a16 16 0 0132 0v7M47 46a14 14 0 0120 13M35 59l6 6 11-12"/>',
    message:'<path d="M16 18h48v34H38L24 64V52h-8z" fill="#fff7fb"/><path d="M26 29h28M26 39h21"/>',
    calendar:'<rect x="18" y="21" width="44" height="42" rx="7" fill="#fff7fb"/><path d="M18 33h44M29 15v13M51 15v13M28 47l8 8 17-14"/>',
    record:'<rect x="22" y="18" width="38" height="48" rx="6" fill="#fff7fb"/><rect x="31" y="13" width="20" height="10" rx="3"/><path d="M31 35h20M31 45h20M31 55h13"/>',
    clock:'<circle cx="40" cy="40" r="25" fill="#fff7fb"/><path d="M40 23v18l12 8"/>',
    ignore:'<path d="M18 21h44v34H42L29 64v-9H18z" fill="#fff7fb"/><path d="M30 31l20 14M50 31L30 45"/>'
  };
  function careIcon(key){
    if(key==='fruit')return (root.foodIcon||module.exports.foodIcon)('Fruta');
    if(key==='tea')return (root.foodIcon||module.exports.foodIcon)('Infusión');
    return '<svg viewBox="0 0 80 80" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg"><circle cx="40" cy="40" r="38" fill="#f8e5ee"/><g fill="#e6b8ce" stroke="#83355f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'+(drawings[key]||drawings.care)+'</g></svg>';
  }
  if(typeof module!=='undefined'&&module.exports)module.exports.careIcon=careIcon;else root.careIcon=careIcon;
})(typeof window!=='undefined'?window:globalThis);
