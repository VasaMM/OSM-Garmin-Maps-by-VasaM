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
echo - Instalce mapy do Mapsource/Basecamp
echo - 
echo - Mapa:  "%NAME% - VasaM"
echo -  FID:  %ID%
echo -  PID:  1
echo - 
echo - Instalaci zrusite stiskem Ctrl-C.
echo - 
pause
 
echo Zapisuji do registru:.
 
set KEY=HKLM\SOFTWARE\Wow6432Node\Garmin\MapSource
if %PROCESSOR_ARCHITECTURE% == AMD64 goto key_ok
set KEY=HKLM\SOFTWARE\Garmin\MapSource
:key_ok
 
reg ADD %KEY%\Families\FAMILY_%ID% /v ID /t REG_BINARY /d %ID_HEX% /f
reg ADD %KEY%\Families\FAMILY_%ID% /v IDX /t REG_SZ /d "%~dp0mapset.mdx" /f
reg ADD %KEY%\Families\FAMILY_%ID% /v MDR /t REG_SZ /d "%~dp0mapset_mdr.img" /f
reg ADD %KEY%\Families\FAMILY_%ID% /v TYP /t REG_SZ /d "%~dp0style.typ" /f
reg ADD %KEY%\Families\FAMILY_%ID%\1 /v Loc /t REG_SZ /d "%~dp0\" /f
reg ADD %KEY%\Families\FAMILY_%ID%\1 /v Bmap /t REG_SZ /d "%~dp0mapset.img" /f
reg ADD %KEY%\Families\FAMILY_%ID%\1 /v Tdb /t REG_SZ /d "%~dp0mapset.tdb" /f
 
:end
pause
exit 0
