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

/* Soft illustrated care icons: warm outlines, rounded shapes and shaded fills. */
(function(root){
  let sequence=0;
  const drawings={
    care:'<rect x="15" y="28" width="50" height="35" rx="11" fill="url(#PINK)"/><path d="M29 28v-8q11-9 22 0v8" fill="none"/><rect x="29" y="35" width="22" height="22" rx="7" fill="#fff9ed"/><path d="M40 39v14M33 46h14" stroke="#c95c7d" stroke-width="5"/>',
    support:'<path d="M10 67V53q3-14 19-14t19 14v14" fill="url(#PINK)"/><path d="M42 67V52q5-11 14-11t17 13v13" fill="#8fcac0"/><circle cx="29" cy="27" r="13" fill="url(#SKIN)"/><circle cx="55" cy="30" r="11" fill="url(#SKIN)"/><path d="M16 27q-2-20 13-18 16 0 13 17l-7-10q-7 9-19 11M45 27q-1-15 11-13 12 0 10 15l-8-9z" fill="#784939"/><path d="M25 31q4 5 8 0M52 34q3 4 6 0" fill="none" stroke-width="2"/>',
    message:'<path d="M13 18h54v36H40L25 66V54H13z" fill="url(#BLUE)"/><path d="M24 30h31M24 40h22" stroke="#fff9f0" stroke-width="5"/><circle cx="61" cy="58" r="11" fill="url(#PINK)"/><path d="M56 58h10M61 53v10" stroke="#fff"/>',
    calendar:'<rect x="16" y="20" width="48" height="46" rx="9" fill="#fff9ed"/><path d="M16 33V27q0-7 8-7h32q8 0 8 7v6" fill="url(#PINK)"/><path d="M28 14v13M52 14v13" stroke-width="5"/><path d="M28 48l9 9 17-16" stroke="#498c7a" fill="none" stroke-width="6"/>',
    record:'<rect x="20" y="17" width="42" height="51" rx="8" fill="url(#BLUE)"/><rect x="25" y="23" width="32" height="39" rx="5" fill="#fff9ed"/><rect x="30" y="12" width="22" height="14" rx="5" fill="#e5b67d"/><path d="M33 38h16M33 47h16M33 56h9" stroke="#668f96"/>',
    clock:'<circle cx="40" cy="42" r="27" fill="#ebbd81"/><circle cx="40" cy="42" r="21" fill="#fffcf2"/><path d="M40 27v16l12 8" fill="none" stroke="#a85675" stroke-width="5"/><path d="M20 15l-7 8M60 15l7 8M24 67l-4 6M56 67l4 6" stroke-width="5"/>',
    ignore:'<path d="M15 20h50v34H40L26 65V54H15z" fill="url(#BLUE)"/><path d="M26 31h28M26 42h19" stroke="#fff9f0"/><circle cx="61" cy="59" r="12" fill="url(#PINK)"/><path d="M56 54l10 10M66 54L56 64" stroke="#fff" stroke-width="4"/>',
    fruit:'<path d="M40 25q-23-14-27 12-2 25 22 30h10q23-6 21-30-5-25-26-12" fill="url(#PINK)"/><path d="M40 25V14" fill="none"/><path d="M42 18q3-17 20-10-2 14-20 10" fill="#8ec49b"/><path d="M24 34q-5 6-3 13" stroke="#ffe8de" stroke-width="5" fill="none"/>',
    tea:'<path d="M59 31h8q15 18-9 23" fill="none" stroke="#b78565" stroke-width="6"/><path d="M14 29h47v22q-2 16-23 16T14 51z" fill="url(#BLUE)"/><ellipse cx="38" cy="29" rx="23" ry="7" fill="#be8b63"/><path d="M29 19q-7-5 0-11M44 18q-6-6 1-12" fill="none" stroke="#b6a28b"/><path d="M10 69h57" stroke="#c7a982" stroke-width="5"/>'
  };
  function careIcon(key){
    const id='care'+sequence++,pink=id+'p',skin=id+'s',blue=id+'b';
    const art=(drawings[key]||drawings.care).replaceAll('PINK',pink).replaceAll('SKIN',skin).replaceAll('BLUE',blue);
    return `<svg viewBox="0 0 80 80" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="${pink}" x2=".8" y2="1"><stop stop-color="#ffb8c2"/><stop offset="1" stop-color="#d77296"/></linearGradient><radialGradient id="${skin}" cx="35%" cy="30%"><stop stop-color="#ffe5c6"/><stop offset="1" stop-color="#e7ae86"/></radialGradient><linearGradient id="${blue}" x2=".8" y2="1"><stop stop-color="#d2ece4"/><stop offset="1" stop-color="#88b8bd"/></linearGradient></defs><circle cx="40" cy="40" r="38" fill="#fff3e5"/><ellipse cx="40" cy="72" rx="25" ry="4" fill="#82533d20"/><g stroke="#785142" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${art}</g></svg>`;
  }
  if(typeof module!=='undefined'&&module.exports)module.exports.careIcon=careIcon;else root.careIcon=careIcon;
})(typeof window!=='undefined'?window:globalThis);
