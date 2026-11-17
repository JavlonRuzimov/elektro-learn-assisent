@echo off
echo ========================================================
echo   ElektroLearn Avtopilot va Telegram Botni ishga tushirish
echo ========================================================
cd /d "%~dp0"

echo Jarayonlar Windows fonida (yashirin) ishga tushirilmoqda...
start "" "C:\Python314\pythonw.exe" autopilot.py
start "" "C:\Python314\pythonw.exe" telegram_bot.py

echo.
echo [OK] Tizim muvaffaqiyatli mustaqil fonga o'tkazildi!
echo Endi Antigravity IDE ni bemalol yopishingiz mumkin.
echo Jarayonni "data/autopilot.log" fayli yoki Telegram botingiz orqali kuzatishingiz mumkin.
echo.
pause
