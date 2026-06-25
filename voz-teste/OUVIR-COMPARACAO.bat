@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   TESTE A/B DE VOZ - THE LONG RUN
echo ============================================
echo.
echo [1/2] Gerando vozes no KOKORO (rapido)...
echo.
"C:\Users\games\miniconda3\envs\worldforge\python.exe" ab_kokoro.py
echo.
echo [2/2] Gerando vozes no CHATTERBOX...
echo       (na 1a vez baixa o modelo ~1GB - pode demorar uns minutos)
echo.
"C:\Users\games\miniconda3\envs\voz\python.exe" ab_chatterbox.py
echo.
echo ============================================
echo   PRONTO! Abrindo a pasta com os audios.
echo   Compare: *_KOKORO.wav  vs  *_CHATTERBOX.wav
echo ============================================
start "" "%~dp0"
pause
