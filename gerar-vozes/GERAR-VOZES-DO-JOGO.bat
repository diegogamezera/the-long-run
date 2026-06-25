@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==================================================
echo   GERAR VOZES DO JOGO - THE LONG RUN (Kokoro)
echo ==================================================
echo.
echo [1/2] Atualizando a lista de falas (manifesto)...
node export-manifest.mjs
echo.
echo [2/2] Gerando as vozes (so o que falta)...
echo       Primeira vez: ~25-35 min. Pode deixar rodando.
echo.
"C:\Users\games\miniconda3\envs\worldforge\python.exe" generate_voices.py
echo.
echo ==================================================
echo   PRONTO! Agora me avisa que eu publico no jogo.
echo ==================================================
pause
