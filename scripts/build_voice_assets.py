"""Build Spanish educational audio on Windows using installed SAPI and lameenc.

Development only: pip install lameenc==1.9.0. No TTS dependency at deployment.
Run from repository root: python scripts/build_voice_assets.py
"""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import wave

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from additional_questions import ADDITIONAL
from feedback_examples import example_for, final_parts, test_risk


def texts():
    tree = ast.parse((ROOT / "app.py").read_text(encoding="utf-8"))
    bank = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "BANCO" for t in n.targets))
    bank.update(ADDITIONAL)
    result = {f"Pregunta {number}." for number in range(1, 11)}
    for stage in bank.values():
        for q in stage:
            example = example_for(q)
            result.add(q["bien"])
            for answer in q["opts"]:
                correct = answer == q["corr"]
                if not correct:
                    result.add(f"Elegiste «{answer}». La respuesta correcta es «{q['corr']}». {q['mal']} {example}")
                row = dict(question=q["q"], selected=answer, answer=q["corr"], correct=correct,
                           feedback=q["bien"] if correct else q["mal"], example=example)
                result.update(final_parts([row], 0, test_risk(0)))
    for score in range(11):
        result.update(final_parts([], score, test_risk(score)))
    return sorted(result)


def main():
    import lameenc
    work = ROOT / ".test-data" / "voice-build"
    work.mkdir(parents=True, exist_ok=True)
    target = ROOT / "voice_assets"
    target.mkdir(exist_ok=True)
    items = [{"id": hashlib.sha256(text.encode()).hexdigest(), "text": text} for text in texts()]
    manifest = work / "texts.json"
    manifest.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8-sig")
    subprocess.run(["powershell.exe", "-NoProfile", "-File", str(ROOT / "scripts" / "synthesize_voice.ps1"),
                    "-Manifest", str(manifest), "-OutputDirectory", str(work)], check=True)
    metadata = {}
    for item in items:
        with wave.open(str(work / (item["id"] + ".wav")), "rb") as wav:
            assert wav.getnchannels() == 1 and wav.getsampwidth() == 2
            encoder = lameenc.Encoder()
            encoder.set_bit_rate(48)
            encoder.set_in_sample_rate(wav.getframerate())
            encoder.set_channels(1)
            encoder.set_quality(2)
            data = bytes(encoder.encode(wav.readframes(wav.getnframes()))) + bytes(encoder.flush())
            assert not data.startswith(b"ID3")
            (target / (item["id"] + ".mp3")).write_bytes(data)
            metadata[item["id"]] = {"seconds": round(wav.getnframes() / wav.getframerate(), 2), "bytes": len(data)}
    (target / "manifest.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Generated {len(items)} Spanish audio clips; {sum(m['bytes'] for m in metadata.values()) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
