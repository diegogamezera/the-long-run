# -*- coding: utf-8 -*-
# A/B de voz - CHATTERBOX  (env: voz)
# Gera as MESMAS 3 falas do script Kokoro, pra comparacao justa.
# Na 1a vez baixa o modelo (~1GB) do HuggingFace - normal.
import os
import soundfile as sf
import torch
from chatterbox.tts import ChatterboxTTS

HERE = os.path.dirname(os.path.abspath(__file__))

LINES = {
    "soren": "Slow. Both hands. No clock that can touch me. Fourteen months under teaches you that. Hurry is a tell.",
    "tib":   "I am extremely for sale. I have a price. It is very high, and it includes a heated compartment and a no-eel clause.",
    "yenna": "I don't get to be free, Halgrave. I get to be useful. I spent six years thinking those were the same prison. They're not. One of them I chose.",
}

# exaggeration = intensidade emocional (0=neutro, ~0.8=bem expressivo)
EXAG = {"soren": 0.4, "tib": 0.8, "yenna": 0.55}

dev = "cuda" if torch.cuda.is_available() else "cpu"
print(f">>> CHATTERBOX: carregando modelo ({dev})... (1a vez baixa ~1GB)")
model = ChatterboxTTS.from_pretrained(device=dev)

# Nota: aqui todos usam a voz padrao do Chatterbox (variando so a emocao).
# No jogo final, cada personagem ganha um clipe de referencia proprio
# (audio_prompt_path) pra ter voz distinta de verdade.
print(">>> CHATTERBOX: gerando 3 falas...")
for who, text in LINES.items():
    wav = model.generate(text, exaggeration=EXAG[who], cfg_weight=0.5)
    out = os.path.join(HERE, f"{who}_CHATTERBOX.wav")
    sf.write(out, wav.squeeze(0).cpu().numpy(), model.sr)
    print(f"  OK  {who:6s} (exag={EXAG[who]})  ->  {os.path.basename(out)}")

print(">>> CHATTERBOX pronto.")
