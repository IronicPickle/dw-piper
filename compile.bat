@echo off
echo What version is this distribution?
set /p version="Enter Version: "
echo %version% > "version"
echo Compiling as version %version%
pause
pyinstaller duct.spec -y --clean
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "./duct.iss" /DAppVersion=%version%
echo Compiled version %version%
( echo ^{ & echo   "date": "%date%", & echo   "version": "%version%", & echo   "changes": [ & echo     "Changes go here" & echo   ] & echo } ) > ./output/%version%/changelog.json
echo Generated template changelog
pause