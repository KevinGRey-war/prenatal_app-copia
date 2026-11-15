"""Spanish voice feedback with sentence-sized queues and visible playback controls."""
import json
import hashlib
import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ASSETS = Path(__file__).resolve().parent / "voice_assets"


def clip_path(text):
    return ASSETS / (hashlib.sha256(text.encode("utf-8")).hexdigest() + ".mp3")


def voice_markup(text):
    payload = json.dumps(str(text), ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e")
    return r"""<!doctype html><html lang="es"><meta charset="utf-8">
    <style>body{margin:0;font:14px 'Segoe UI',sans-serif;color:#624471}button{cursor:pointer;border:1px solid #d9c5e8;background:#fff6fc;color:#624471;border-radius:12px;padding:10px 14px;font:inherit;font-weight:600;margin:0 6px 5px 0}button:focus-visible{outline:3px solid #7c3aed}#status{font-size:12px;margin:2px 0}</style>
    <p id="status" hidden>Preparando la explicación hablada…</p>
    <script>
    const text = PAYLOAD;
    const status = document.getElementById('status');
    let generation=0, active=null;
    function chunks(value){
        const words=value.split(/\s+/), out=[];let line='';
        for(const word of words){if(line.length+word.length>170){out.push(line);line='';}line+=(line?' ':'')+word;}
        if(line)out.push(line);return out;
    }
    function stop(){generation++;if('speechSynthesis' in window)window.speechSynthesis.cancel();active=null;}
    function play(){
        stop();if(!('speechSynthesis' in window)){status.textContent='La voz no está disponible en este navegador. La explicación completa sigue visible en pantalla.';return;}
        const queue=chunks(text), own=generation;let index=0;
        function next(){
            if(own!==generation)return;
            if(index>=queue.length){status.textContent='Explicación terminada. Puedes volver a escucharla.';return;}
            active=new SpeechSynthesisUtterance(queue[index]);active.lang='es-ES';active.rate=.93;active.pitch=1;
            const voices=window.speechSynthesis.getVoices();
            const spanish=voices.find(v=>v.lang.startsWith('es'));
            if(spanish)active.voice=spanish;
            active.onstart=()=>{status.textContent='🔊 Reproduciendo explicación en voz…';};
            active.onend=()=>{index++;next();};
            active.onerror=event=>{if(own!==generation)return;status.textContent=event.error==='not-allowed'?'Pulsa Escuchar explicación para activar la voz en este navegador.':'Pulsa Escuchar explicación para volver a intentar la voz.';};
            window.speechSynthesis.speak(active);
        }
        next();
    }
    window.addEventListener('pagehide',stop);
    setTimeout(play,150);
    </script></html>""".replace("PAYLOAD", payload)


def audio_markup(audio):
    """Embed the recording: avoid the server's failing /media HTTP route."""
    source = base64.b64encode(audio).decode("ascii")
    return '''<!doctype html><html lang="es"><meta charset="utf-8">
    <style>body{margin:0;color:#624471;font:14px 'Segoe UI',sans-serif}audio{width:100%}p{margin:4px 0}</style>
    <audio id="voice" hidden autoplay preload="auto" aria-label="Explicación en voz" src="data:audio/mpeg;base64,''' + source + '''"></audio>
    <p id="status" hidden>Preparando voz…</p>
    <script>
    const audio=document.getElementById('voice'), status=document.getElementById('status');
    audio.addEventListener('playing',()=>status.textContent='🔊 Reproduciendo voz');
    audio.addEventListener('ended',()=>status.textContent='Explicación terminada.');
    audio.addEventListener('pause',()=>{if(!audio.ended)status.textContent='Voz en pausa.';});
    audio.addEventListener('error',()=>status.textContent='No se pudo reproducir la voz.');
    audio.play().catch(()=>status.textContent='El navegador bloqueó la voz automática. Pulsa reproducir para escuchar.');
    window.addEventListener('pagehide',()=>audio.pause());
    </script></html>'''


def hablar(text, parts=None):
    clips = [clip_path(part) for part in (parts or [text])]
    if clips and all(path.is_file() for path in clips):
        # CBR MP3 clips have matching encodings and no ID3/Xing headers, so their
        # frames can be concatenated into a single player with seek/replay.
        audio = b"".join(path.read_bytes() for path in clips)
        components.html(audio_markup(audio), height=0)
    else:
        components.html(voice_markup(text), height=0)
