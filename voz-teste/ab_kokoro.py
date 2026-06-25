# -*- coding: utf-8 -*-
# A/B de voz - KOKORO  (env: worldforge)
# Gera 3 falas representativas do jogo, uma por personagem.
import os, sys
import numpy as np
import soundfile as sf
from kokoro import KPipeline

HERE = os.path.dirname(os.path.abspath(__file__))

# As MESMAS falas usadas no script do Chatterbox (comparacao justa)
LINES = {
    "soren": "Slow. Both hands. No clock that can touch me. Fourteen months under teaches you that. Hurry is a tell.",
    "tib":   "I am extremely for sale. I have a price. It is very high, and it includes a heated compartment and a no-eel clause.",
    "yenna": "I don't get to be free, Halgrave. I get to be useful. I spent six years thinking those were the same prison. They're not. One of them I chose.",
}

# Elenco de vozes Kokoro (a* = ingles americano, b* = britanico)
VOICE = {"soren": "am_michael", "tib": "bm_george", "yenna": "bf_emma"}

pipes = {}
def pipe_for(voice):
    lc = "b" if voice[0] == "b" else "a"
    if lc not in pipes:
        pipes[lc] = KPipeline(lang_code=lc)
    return pipes[lc]

print(">>> KOKORO: gerando 3 falas...")
for who, text in LINES.items():
    v = VOICE[who]
    p = pipe_for(v)
    chunks = [audio for _, _, audio in p(text, voice=v)]
    if not chunks:
        print("  ERRO: nada gerado para", who); continue
    audio = np.concatenate(chunks)
    out = os.path.join(HERE, f"{who}_KOKORO.wav")
    sf.write(out, audio, 24000)
    print(f"  OK  {who:6s} ({v})  ->  {os.path.basename(out)}")

print(">>> KOKORO pronto.")
