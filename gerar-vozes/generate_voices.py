# -*- coding: utf-8 -*-
# Gera a voz de TODAS as falas do jogo com KOKORO (env: worldforge).
# Le gerar-vozes/audio-manifest.json e escreve em the-long-run/audio/<id>.mp3
# Pula falas que ja existem -> rodar de novo so gera o que falta/mudou.
import os, sys, json, subprocess
import numpy as np
import soundfile as sf
from kokoro import KPipeline

HERE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(HERE)
AUDIO = os.path.join(ROOT, "audio")
os.makedirs(AUDIO, exist_ok=True)

manifest = json.load(open(os.path.join(HERE, "audio-manifest.json"), encoding="utf-8"))

# ---- ELENCO DE VOZES (mude aqui se quiser trocar) ----
VOICE = {
    "soren": "am_michael",   # narrador grave/calmo (ingles americano)
    "tib":   "bm_george",    # comico (ingles britanico)
    "yenna": "bf_emma",      # feminina grave (britanico)
}
# sys = sem voz (sao etiquetas do sistema)

pipes = {}
def pipe_for(voice):
    lc = "b" if voice[0] == "b" else "a"
    if lc not in pipes:
        pipes[lc] = KPipeline(lang_code=lc)
    return pipes[lc]

def have_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True)
        return True
    except Exception:
        return False
FF = have_ffmpeg()
EXT = "mp3" if FF else "wav"

todo = [m for m in manifest if m["who"] in VOICE]
total = len(todo)
print(f">>> KOKORO: {total} falas para gerar (formato {EXT}). Pulando as que ja existem.")

made = skip = fail = 0
for n, item in enumerate(todo, 1):
    aid, who, text = item["id"], item["who"], item["text"]
    final = os.path.join(AUDIO, f"{aid}.{EXT}")
    if os.path.exists(final):
        skip += 1
        continue
    try:
        v = VOICE[who]
        chunks = [a for _, _, a in pipe_for(v)(text, voice=v)]
        if not chunks:
            print("  ! vazio:", aid); fail += 1; continue
        audio = np.concatenate(chunks)
        wav = os.path.join(AUDIO, f"{aid}.wav")
        sf.write(wav, audio, 24000)
        if FF:
            subprocess.run(
                ["ffmpeg", "-y", "-i", wav, "-codec:a", "libmp3lame", "-q:a", "4",
                 os.path.join(AUDIO, f"{aid}.mp3")],
                capture_output=True,
            )
            os.remove(wav)
        made += 1
        if made % 20 == 0:
            print(f"  ... {made} geradas  ({n}/{total})")
    except Exception as e:
        print("  ! erro em", aid, "->", e); fail += 1

# sinaliza pro jogo que o audio esta pronto + diz o formato
json.dump({"ready": True, "format": EXT, "count": made + skip},
          open(os.path.join(AUDIO, "ready.json"), "w"))

print(f">>> PRONTO. Novas: {made} | Ja existiam: {skip} | Falhas: {fail} | Formato: {EXT}")
print(f">>> Audios em: {AUDIO}")
