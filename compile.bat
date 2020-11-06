@echo off
echo What version is this distribution?
set /p version="Enter Version: "
echo %version% > "version"
echo Compiling as version %version%
pause
pyinstaller dw.spec -y --clean
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "./dw-piper.iss" /DAppVersion=%version%
echo Compiled version %version%
( echo ^> Changelog ^(%date%^) & echo ^> Version: %version% & echo. & echo - First change & echo - Another change ) > ./output/%version%/changelog.txt
echo Generated template changelog
pause