@echo off
goto check_Permissions
 
:check_Permissions
net session >nul 2>&1
if %errorLevel% == 0 (
    goto main
) else (
    echo CHYBA: Spuste skript jako administrator!
    goto end
)
 
:main
echo - Odinstalace mapy z Mapsource/Basecamp
echo - 
echo - Mapa:  "%NAME% - VasaM"
echo -  FID:  %ID%
echo -  PID:  1
echo - 
echo - Instalaci zrusite stiskem Ctrl-C.
echo - 
pause
 
set KEY=HKLM\SOFTWARE\Wow6432Node\Garmin\MapSource
if %PROCESSOR_ARCHITECTURE% == AMD64 goto key_ok
set KEY=HKLM\SOFTWARE\Garmin\MapSource
:key_ok
 
reg DELETE %KEY%\Families\FAMILY_%ID% /f
:end
pause
exit 0
