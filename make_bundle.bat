@echo off
echo Creating SKELOS Distribution Bundle...
mkdir "C:\SKELOS_DISTRIBUTION"
xcopy /E /I "C:\skelos app\skelos" "C:\SKELOS_DISTRIBUTION\skelos"
copy "C:\skelos app\requirements.txt" "C:\SKELOS_DISTRIBUTION\requirements.txt"
copy "C:\skelos app\Run_SKELOS.bat" "C:\SKELOS_DISTRIBUTION\Run_SKELOS.bat"
echo.
echo Bundle created successfully at C:\SKELOS_DISTRIBUTION
echo Now you can right-click this folder and "Compress to ZIP file".
pause
